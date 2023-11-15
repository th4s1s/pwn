#!/bin/sh
set -e
set -x

# Chown the mounted data volume
chown -R service:service "/data/"
chown -R service:service "/service/"
nginx
# Install the dependencies
su -s /bin/sh -c 'npm install' service
# Start the server
echo "Starting server..."
exec su -s /bin/sh -c 'node /service/server.js' service