#!/usr/bin/env bash

source /scripts/functions.sh

download_geoserver
download_extensions
setup_environment
update_webcors

set -m
catalina.sh run &
/scripts/startup_config.sh
fg %1