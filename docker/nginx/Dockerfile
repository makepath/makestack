FROM nginx:alpine

ARG ENV

# Dependencies
RUN apk add --no-cache certbot bash

# Copy Nginx config files
ADD docker/nginx/files/ /etc/nginx/

RUN if [ "$ENV" == "prod" ] ; \
    then mv /etc/nginx/nginx_prod.conf /etc/nginx/nginx.conf ; \
    else mv /etc/nginx/nginx_dev.conf /etc/nginx/conf.d/default.conf ; fi

# Copy scripts
COPY ./docker/nginx/scripts /scripts

# Add execute permission to scripts
RUN chmod +x /scripts/*.sh

CMD ["/scripts/entrypoint.sh"]