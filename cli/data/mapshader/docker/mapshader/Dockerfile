FROM python:3.9.9-slim-buster

# Enviroment
ENV HOMEAPP=/code
ENV PATH=$PATH:$HOMEAPP/.local/bin

WORKDIR $HOMEAPP/

# Dependencies
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    bash \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Using a non-privileged user to own our code
RUN useradd -d $HOMEAPP -N non-privileged \
    && chown -R non-privileged $HOMEAPP

# Code
RUN pip3 install mapshader==0.1.1

USER non-privileged