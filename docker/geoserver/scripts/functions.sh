#!/usr/bin/env bash

function download_geoserver() {
    echo "Downloading GeoServer"

    wget -q -O /tmp/geoserver.zip "${GEOSERVER_DOWNLOAD_URL}"
    unzip -j -o /tmp/geoserver.zip "geoserver.war" -d /tmp/
    unzip /tmp/geoserver.war -d ${CATALINA_HOME}/webapps/geoserver

    rm /tmp/geoserver.war
    rm /tmp/geoserver.zip
}

function download_extensions() {
    echo "Downloading extensions"

    for plugin in $(cat ${CONFIG_DIR}/extensions.txt); do
        wget -q -O /tmp/extension.zip "${GEOSERVER_EXTENSION_BASE_URL}/${plugin}.zip"
        unzip -d ${CATALINA_HOME}/webapps/geoserver/WEB-INF/lib /tmp/extension.zip
        rm /tmp/extension.zip
    done
}


function setup_environment() {
    echo "Setting up the environment"

    export GEOSERVER_OPTS="-Duser.timezone=UTC \
                           -DGEOSERVER_CSRF_DISABLED=true \
                           -Dgeoserver.xframe.shouldSetPolicy=false"
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
                          -Dlog4j.configuration=${CONFIG_DIR}/log4j.properties \
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
    echo "Adding proxy url"

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

function update_webcors() {
    echo "Updating webcors"

    rm ${CATALINA_HOME}/conf/web.xml
    rm ${CATALINA_HOME}/webapps/geoserver/WEB-INF/web.xml
    cp -f ${CONFIG_DIR}/tomcat.xml  ${CATALINA_HOME}/conf/web.xml
    cp -f ${CONFIG_DIR}/geoserver.xml ${CATALINA_HOME}/webapps/geoserver/WEB-INF/web.xml
}