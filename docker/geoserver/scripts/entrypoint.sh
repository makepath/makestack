#!/usr/bin/env bash

source /scripts/functions.sh

download_geoserver
setup_environment

set -m
catalina.sh run &
/scripts/startup_config.sh
fg %1