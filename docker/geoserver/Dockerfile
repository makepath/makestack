FROM tomcat:9.0-jdk11-openjdk-slim-buster

# Enviroment
ENV CATALINA_BASE=${CATALINA_HOME}

# Dependencies
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    bash \
    fontconfig \
    libfreetype6 \
    postgresql-client \
    unzip \
    wget \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Using a non-privileged user to own our code
RUN useradd -d ${CATALINA_HOME} -N non-privileged \
    && chown -R non-privileged ${CATALINA_HOME}

# Copy scripts
COPY --chown=non-privileged:nogroup ./docker/geoserver/scripts /scripts

# Copy extra config
COPY --chown=non-privileged:nogroup ./docker/geoserver/log4j.properties /

# Add execute permission to scripts
RUN chmod +x /scripts/*.sh

USER non-privileged

CMD ["/scripts/entrypoint.sh"]