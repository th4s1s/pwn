#!/bin/bash

NUMBER_OF_ROUNDS=12
DATABASE_PATH="/var/www/html/Database/db.sqlite"
FILES_DIRECTORY="/var/www/html/files"

currentTime=$(date +%s)
deletionTime=$((currentTime - NUMBER_OF_ROUNDS*60))

sqlite3 "$DATABASE_PATH" "DELETE FROM user WHERE created_at < $deletionTime;"
sqlite3 "$DATABASE_PATH" "DELETE FROM complaint WHERE user_id NOT IN (SELECT id FROM user) OR submitted_at < $deletionTime;"

filenames=$(sqlite3 "$DATABASE_PATH" "SELECT recipe.filename FROM recipe WHERE user_id NOT IN (SELECT id FROM user);")

for filename in $filenames; do
  if [ -f "$filename" ]; then
    rm "$filename"
    echo "Removed file: $filename"
  else
    echo "File not found: $filename"
  fi
done

sqlite3 "$DATABASE_PATH" "DELETE FROM recipe WHERE user_id NOT IN (SELECT id FROM user);"

find "$FILES_DIRECTORY" -empty -type d -delete -mindepth 1
