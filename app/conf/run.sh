#!/bin/bash
poetry shell;
python manage.py collectstatic --noinput
python manage.py migrate
python3 manage.py createsuperuser --noinput

# start nginx
sed -i 's,NGINX_SET_REAL_IP_FROM,'"$NGINX_SET_REAL_IP_FROM"',g' /etc/nginx/nginx.conf
sed -i 's,UWSGI_SOCKET,'"$UWSGI_SOCKET"',g' /etc/nginx/conf.d/app.conf
sed -i 's,UWSGI_CHDIR,'"$UWSGI_CHDIR"',g' /etc/nginx/conf.d/app.conf

nginx
uwsgi /app/uwsgi/uwsgi.ini
