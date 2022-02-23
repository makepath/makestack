#!/usr/bin/env bash

FILE=/etc/nginx/nginx_dev.conf

if [ -e "$FILE" ]; then
    # Get certificate
    certbot certonly --standalone -d mapstack.eastus.cloudapp.azure.com --email giancarlo@makepath.com -n --agree-tos --expand

    # Start nginx
    /usr/sbin/nginx -g "daemon off;"

    while [ true ]; do
        # Renew certificate and tell nginx to reload its config
        certbot renew --webroot --webroot-path /var/lib/certbot/ --post-hook "nginx -s reload"

        # Sleep for 1 week
        sleep 604810
    done
else
    # Start nginx
    /usr/sbin/nginx -g "daemon off;"
fi
