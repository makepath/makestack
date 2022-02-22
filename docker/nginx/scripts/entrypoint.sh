#!/usr/bin/env bash

envsubst < /tmp/nginx.conf > /etc/nginx/conf.d/default.conf
sed -i 's/§/$/g' /etc/nginx/conf.d/default.conf

nginx -g 'daemon off;'