FROM python:3.9.9-slim-buster

# Enviroment
ENV HOMEAPP=/code
ENV PATH=$PATH:$HOMEAPP/.local/bin
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

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
RUN useradd -d $HOMEAPP -N non-privileged

# Update non-privileged user folder permission
RUN chown -R non-privileged $HOMEAPP

# Python requirements
COPY ./backend/requirements.txt $HOMEAPP/requirements.txt
COPY ./backend/requirements-test.txt $HOMEAPP/requirements-test.txt

RUN pip3 install -r requirements.txt \
    && pip3 install -r requirements-test.txt

# Code
COPY --chown=non-privileged:nogroup ./backend $HOMEAPP/

USER non-privileged