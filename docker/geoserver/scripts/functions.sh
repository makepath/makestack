#!/usr/bin/env bash

function download_geoserver() {
    echo "Downloading GeoServer"

    wget -q -O ${CATALINA_HOME}/webapps/geoserver.zip "${GEOSERVER_DOWNLOAD_URL}"
    unzip -j -o ${CATALINA_HOME}/webapps/geoserver.zip "geoserver.war" -d ${CATALINA_HOME}/webapps
    rm ${CATALINA_HOME}/webapps/geoserver.zip
}

function setup_environment() {
    echo "Setting up the environment"

    export GEOSERVER_OPTS="-Duser.timezone=UTC"
    export ENV JAVA_OPTS="-Djava.awt.headless=true -server \
                          -Xms${GEOSERVER_INITIAL_MEMORY} \
                          -Xmx${GEOSERVER_MAXIMUM_MEMORY} \
                          -XX:PerfDataSamplingInterval=500 \
                          -XX:SoftRefLRUPolicyMSPerMB=46000 \
                          -XX:NewRatio=2 \
                          -XX:+UseG1GC \
                          -XX:MaxGCPauseMillis=200 \
                          -XX:ParallelGCThreads=20 \
                          -XX:ConcGCThreads=5 \
                          -XX:InitiatingHeapOccupancyPercent=45 \
                          -XX:+CMSClassUnloadingEnabled \
                          -Dfile.encoding=UTF8 \
                          -Djavax.servlet.request.encoding=UTF-8 \
                          -Djavax.servlet.response.encoding=UTF-8 \
                          -Dlog4j.configuration=${CATALINA_HOME}/log4j.properties \
                          ${GEOSERVER_OPTS}"
}

function update_admin_password() {
    echo "Updating admin password"

    ADMIN_HEADER=$(echo -n "admin:geoserver" | base64)
    curl -s -H "Authorization: basic $ADMIN_HEADER" \
         -X PUT http://localhost:8080/geoserver/rest/security/self/password \
         -H  "accept: application/json" \
         -H  "content-type: application/json" \
         -d "{  \"newPassword\": \"$GEOSERVER_ADMIN_PASSWORD\"}" > /dev/null
}

function add_proxy_url() {
    echo "Updating admin password"

    ADMIN_HEADER=$(echo -n "admin:admin" | base64)
    curl -s -H "Authorization: basic $ADMIN_HEADER" \
            -X PUT http://localhost:8080/geoserver/rest/settings \
            -H  "accept: application/json" \
            -H  "content-type: application/json" \
            -d "{
                    \"global\":
                        {
                            \"useHeadersProxyURL\": true,
                            \"proxyBaseUrl\": \"${GEOSERVER_PROXY_BASE_URL}\"
                        }
                }" > /dev/null
}