#!/bin/sh

set -euo pipefail

case "$1" in
  www)
    echo "$TLS_CERTIFICATE" > /etc/nginx/cert.pem
    echo "$TLS_PRIVATE_KEY" > /etc/nginx/key.pem

    nginx
    sudo -u nginx daphne -u /app/sock/daphne --proxy-headers virtualbarcamp.asgi:application 2>/dev/null
    ;;

  migrate)
    sudo -u nginx ./manage.py migrate
    ;;

  worker)
    sudo -u nginx celery -A virtualbarcamp worker -l info
    ;;

  beat)
    sudo -u nginx celery -A virtualbarcamp beat -l info -S django --pidfile=/tmp/celerybeat.pid
    ;;

  *)
    echo "Usage: $0 {www|worker|beat}"
esac
