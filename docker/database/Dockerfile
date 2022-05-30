FROM postgres:13.4

# Enviroment
ENV POSTGIS_MAJOR 3
ENV POSTGIS_VERSION 3.2.1+dfsg-1.pgdg110+1

RUN apt-get update \
      && apt-cache showpkg postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR \
      && apt-get install -y --no-install-recommends \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR=$POSTGIS_VERSION \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts \
           gdal-bin \
           unzip \
           wget \
      && rm -rf /var/lib/apt/lists/*

# Create folders
RUN mkdir -p /docker-entrypoint-initdb.d

# Copy script files
COPY ./docker/database/scripts/initdb-postgis.sh /docker-entrypoint-initdb.d/10_postgis.sh
COPY ./docker/database/scripts/update-postgis.sh /usr/local/bin