FROM nginx:stable-alpine

# COPY site.template /etc/nginx/conf.d/site.template
CMD ["/bin/sh", "-c", "sed -i 's/listen  .*/listen 8001;/g' /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'"]
EXPOSE 8001