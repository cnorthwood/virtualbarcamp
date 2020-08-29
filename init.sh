#!/bin/sh

set -euo pipefail

case "$0" in
  www)
    echo "$TLS_CERTIFICATE" > /etc/nginx/cert.pem
    echo "$TLS_PRIVATE_KEY" > /etc/nginx/key.pem

    nginx
    su -u nginx -c 'daphne -u /app/sock/daphne --proxy-headers virtualbarcamp.asgi:application' 2>/dev/null
    ;;

  migrate)
    su -u nginx -c './manage.py migrate'
    ;;

  worker)
    su -u nginx -c 'celery -A virtualbarcamp worker -l info'
    ;;

  beat)
    su -u nginx -c 'celery -A virtualbarcamp beat -l info -S django --pidfile=/tmp/celerybeat.pid'
    ;;

  *)
    echo "Usage: $0 {www|worker|beat}"
esac
