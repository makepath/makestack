FROM node:14.15

# Enviroment
ENV HOMEAPP=/code

WORKDIR $HOMEAPP/

# Using a non-privileged user to own our code
RUN useradd -d $HOMEAPP -N non-privileged \
    && chown -R non-privileged $HOMEAPP

USER non-privileged