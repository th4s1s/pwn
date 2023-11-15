FROM php:8.2-fpm

ENV TZ=UTC+2
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt install -y sqlite3 nginx

COPY ./bollwerk/docker/config/php.ini /usr/local/etc/php/conf.d/app.ini

COPY ./bollwerk/app /var/www/html

COPY ./bollwerk/docker/scripts/entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh
COPY ./bollwerk/docker/scripts/cleanup.sh /root/cleanup.sh
RUN chmod +x /root/cleanup.sh

WORKDIR /var/www/html

ENTRYPOINT /root/entrypoint.sh
