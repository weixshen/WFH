# nginx-gunicorn-django

FROM index.alauda.cn/library/ubuntu
MAINTAINER Guoyi <njuguoyi@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python python-pip python-virtualenv nginx gunicorn supervisor

# Setup django application
RUN mkdir -p /deploy/app
COPY app /deploy/app
RUN pip install -r /deploy/app/requirements.txt

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY django.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled/django.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

# Start processes
CMD ["/usr/bin/supervisord"]
