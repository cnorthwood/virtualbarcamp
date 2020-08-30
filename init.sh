#!/bin/sh

set -euo pipefail

case "$1" in
  www)
    echo "$TLS_CERTIFICATE" > /etc/nginx/cert.pem
    echo "$TLS_PRIVATE_KEY" > /etc/nginx/key.pem

    nginx
    sudo -Eu nginx daphne -u /app/sock/daphne --proxy-headers virtualbarcamp.asgi:application
    ;;

  migrate)
    sudo -Eu nginx ./manage.py migrate
    ;;

  worker)
    sudo -Eu nginx celery -A virtualbarcamp worker -l info
    ;;

  beat)
    sudo -Eu nginx celery -A virtualbarcamp beat -l info -S django --pidfile=/tmp/celerybeat.pid
    ;;

  *)
    echo "Usage: $0 {www|worker|beat}"
esac
