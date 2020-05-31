FROM fedora:32 as dev-base

RUN dnf upgrade -y && \
        dnf install -y poetry python3 python3-pip python3-devel python3-setuptools file gcc gcc-c++ make automake autoconf libtool openssl-devel pcre-devel
RUN mkdir /build
WORKDIR /build
RUN curl -Lo watchman.tar.gz https://github.com/facebook/watchman/archive/v4.9.0.tar.gz && \
        tar zxvf watchman.tar.gz && \
        cd watchman-4.9.0 && \
        ./autogen.sh && \
        ./configure --enable-lenient && \
        make && \
        make install

FROM fedora:32 AS builder

RUN dnf install -y 'dnf-command(config-manager)'
RUN dnf config-manager --add-repo https://dl.yarnpkg.com/rpm/yarn.repo
RUN dnf install -y poetry yarn
COPY . /app
WORKDIR /app
RUN yarn
RUN yarn build
RUN poetry export -f requirements.txt -o /app/requirements.txt

FROM fedora:32

RUN dnf upgrade -y && \
        dnf install -y nginx python3-pip gcc
COPY --from=builder /app/requirements.txt /app/manage.py /app/
COPY --from=builder /app/virtualbarcamp/ /app/virtualbarcamp/
COPY --from=builder /app/build/ /app/build/
COPY --from=builder /app/nginx.conf /etc/nginx/nginx.conf
RUN pip install -r /app/requirements.txt
RUN mkdir -p /app/sock && chown nginx:nginx /app/sock

WORKDIR /app
RUN python3 manage.py collectstatic --no-input
CMD nginx; su -u nginx -c 'daphne -u /app/sock/daphne --proxy-headers virtualbarcamp.asgi:application' 2>/dev/null
