#!/bin/bash

touch /var/www/html/Database/db.sqlite
sqlite3 /var/www/html/Database/db.sqlite < /var/www/html/Database/create_database.sql

FILE_DIRECTORY=/var/www/html/files

if [ ! -d "$FILE_DIRECTORY" ]; then
  mkdir "$FILE_DIRECTORY"
fi

chmod 777 "$FILE_DIRECTORY"

chmod 777 /var/www/html/Database/{.,db.sqlite}

/etc/init.d/nginx start

while true; do
	/root/cleanup.sh
	sleep 60
done &

php-fpm
