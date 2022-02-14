#!/usr/bin/env bash

function download_geoserver() {
    wget -O ${CATALINA_HOME}/webapps/geoserver.zip "${GEOSERVER_URL}"
    unzip -j ${CATALINA_HOME}/webapps/geoserver.zip "geoserver.war" -d ${CATALINA_HOME}/webapps
    rm ${CATALINA_HOME}/webapps/geoserver.zip
}

function setup() {
    export GEOSERVER_LOG_DIR="${CATALINA_HOME}/logs"
    export GEOSERVER_DATA_DIR="${CATALINA_HOME}/datadir"
    export GEOSERVER_LOG_LOCATION="${GEOSERVER_LOG_DIR}/geoserver.log"
    export GEOWEBCACHE_CONFIG_DIR="${CATALINA_HOME}/datadir/gwc"
    export GEOWEBCACHE_CACHE_DIR="${CATALINA_HOME}/gwc_cache_dir"
    export NETCDF_DATA_DIR="${CATALINA_HOME}/netcdf_data_dir"
    export GRIB_CACHE_DIR="${CATALINA_HOME}/grib_cache_dir"
    export GEOSERVER_OPTS="-Duser.timezone=UTC \
                           -Dorg.geotools.shapefile.datetime=true \
                           -DGEOSERVER_LOG_LOCATION=${GEOSERVER_LOG_LOCATION} \
                           -DGEOWEBCACHE_CONFIG_DIR=${GEOWEBCACHE_CONFIG_DIR} \
                           -DGEOWEBCACHE_CACHE_DIR=${GEOWEBCACHE_CACHE_DIR} \
                           -DNETCDF_DATA_DIR=${NETCDF_DATA_DIR} \
                           -DGRIB_CACHE_DIR=${GRIB_CACHE_DIR} \
                           -Dlog4j.configuration=${CATALINA_HOME}/log4j.properties"
    export ENV JAVA_OPTS="-Xms${INITIAL_MEMORY} -Xmx${MAXIMUM_MEMORY} \
                          -Djava.awt.headless=true -server \
                          -Dfile.encoding=UTF8 \
                          -Djavax.servlet.request.encoding=UTF-8 \
                          -Djavax.servlet.response.encoding=UTF-8 \
                          -XX:SoftRefLRUPolicyMSPerMB=36000 -XX:+UseG1GC \
                          -XX:MaxGCPauseMillis=200 -XX:ParallelGCThreads=20 -XX:ConcGCThreads=5 \
                          ${GEOSERVER_OPTS}"


    mkdir -p  ${GEOSERVER_LOG_DIR} \
              ${GEOSERVER_DATA_DIR} \
              ${GEOSERVER_LOG_LOCATION} \
              ${GEOWEBCACHE_CONFIG_DIR} \
              ${GEOWEBCACHE_CACHE_DIR} \
              ${NETCDF_DATA_DIR} \
              ${GRIB_CACHE_DIR}
}