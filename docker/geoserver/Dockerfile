FROM tomcat:9.0-jdk11-openjdk-slim-buster

# Enviroment
ENV CATALINA_BASE=${CATALINA_HOME} \
    GEOSERVER_DATA_DIR=/opt/geoserver/data_dir \
    GEOWEBCACHE_CACHE_DIR=/opt/geoserver/data_dir/gwc

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
    wget \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Create volume folders
RUN mkdir -p ${GEOSERVER_DATA_DIR} \
             ${GEOWEBCACHE_CACHE_DIR}

# Copy scripts
COPY ./docker/geoserver/scripts /scripts

# Create a non-privileged user
RUN useradd -d ${CATALINA_HOME} -N non-privileged

# Make the non-privileged user the owner of the folders
RUN chown -R non-privileged ${CATALINA_HOME} \
                            ${GEOSERVER_DATA_DIR} \
                            ${GEOWEBCACHE_CACHE_DIR} \
                            /scripts

# Add execute permission to scripts
RUN chmod +x /scripts/*.sh

USER non-privileged

CMD ["/scripts/entrypoint.sh"]