#!/bin/bash -x

if [ $1 == "prod" ]; then
    mv /tmp/nginx_prod.conf /etc/nginx/user_conf.d/nginx_prod.conf
else
    mv /tmp/nginx_dev.conf /etc/nginx/user_conf.d/nginx_dev.conf
fi