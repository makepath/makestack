FROM tomcat:9.0-jdk11-openjdk-slim-buster

# Enviroment
ENV CATALINA_BASE=${CATALINA_HOME} \
    GEOSERVER_DATA_DIR=/opt/geoserver/data_dir \
    GEOWEBCACHE_CACHE_DIR=/opt/geoserver/data_dir/gwc \
    SCRIPTS_DIR=/scripts \
    CONFIG_DIR=/settings

# Dependencies
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    bash \
    curl \
    fontconfig \
    libfreetype6 \
    postgresql-client \
    unzip \
    vim \
    wget \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Create folders
RUN mkdir -p ${GEOWEBCACHE_CACHE_DIR} \
             ${SCRIPTS_DIR} \
             ${CONFIG_DIR}

# Copy scripts
COPY ./docker/geoserver/scripts ${SCRIPTS_DIR}

# Copy config files
COPY ./docker/geoserver/config ${CONFIG_DIR}

# Create a non-privileged user
RUN addgroup --gid 333 non-privileged && \
    useradd --uid 333 --gid 333 --home-dir /home/non-privileged non-privileged

# Make the non-privileged user the owner of the folders
RUN chown -R non-privileged ${CATALINA_HOME} \
                            ${GEOSERVER_DATA_DIR} \
                            ${GEOWEBCACHE_CACHE_DIR} \
                            ${SCRIPTS_DIR} \
                            ${CONFIG_DIR}

# Add execute permission to scripts
RUN chmod +x /scripts/*.sh

USER non-privileged

CMD ["/scripts/entrypoint.sh"]