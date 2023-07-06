FROM python:3.10-bullseye
LABEL Jungsik Hwang <rootsik1221@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y nginx
RUN mkdir -p /app/uwsgi && \
    mkdir -p /app/server

ADD . /app/server
WORKDIR /app/server

RUN pip install --upgrade pip
RUN pip install uwsgi
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

ENV NGINX_SET_REAL_IP_FROM="172.18.0.0/16"\
    UWSGI_SOCKET="/app/uwsgi/app.sock"\
    UWSGI_PID="/app/uwsgi/app.pid"\
    UWSGI_CHDIR="/app/server"\
    UWSGI_MODULE="tester.wsgi"

RUN mv ./conf/run.sh /
RUN chmod 777 /run.sh
RUN mv ./conf/nginx.conf /etc/nginx/nginx.conf
RUN mv ./conf/app.conf /etc/nginx/conf.d/app.conf
RUN mv ./conf/uwsgi.ini /app/uwsgi/uwsgi.ini

EXPOSE 80 443

CMD ["/run.sh"]
