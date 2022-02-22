FROM nginx:1.21.6

# Copy Nginx config file
COPY ./docker/nginx/files/nginx.conf /tmp/nginx.conf

# Copy scripts
COPY ./docker/nginx/scripts /scripts

# Add execute permission to scripts
RUN chmod +x /scripts/*.sh

CMD ["/scripts/entrypoint.sh"]