FROM python:3.9.9-slim-buster

# Enviroment
ENV HOMEAPP=/code

WORKDIR $HOMEAPP/

# Dependencies
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    gcc \
    libpq-dev \
    python3-dev \
    postgresql-client \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Using a non-privileged user to own our code
RUN useradd -d $HOMEAPP -N non-privileged \
    && chown -R non-privileged $HOMEAPP

# Code
COPY --chown=non-privileged:nogroup ./backend $HOMEAPP/
RUN pip3 install -r requirements.txt

USER non-privileged