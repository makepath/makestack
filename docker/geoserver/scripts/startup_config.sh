#!/usr/bin/env bash

source /scripts/functions.sh

while [ "$(curl -s --retry-connrefused --retry 100 -I http://localhost:8080/geoserver/web/ 2>&1 | grep 200)" == "" ]; do
    sleep 5
done

update_admin_password

if [[ "$GEOSERVER_PROXY_BASE_URL" ]]; then
    add_proxy_url
fi