FROM node:14.15-buster-slim AS Client
WORKDIR /webapp/frontend
COPY frontend/package.json ./package.json
RUN mkdir -p /webapp/backend/templates
RUN mkdir -p /webapp/backend/static
RUN npm install
COPY frontend .
RUN npm run build && ls -R /webapp/backend/static



FROM python:3.8.7-slim-buster AS Django
# set environment variables
# install psycopg2 dependencies
WORKDIR /webapp/backend
COPY backend/requirements.txt ./requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev \
    python3-dev \
    libgeos-dev \
    build-essential \
    unixodbc-dev \
    netcat \
    shapelib \
    libproj-dev \
    && ln -s /usr/lib/libproj.so.0 /usr/lib/libproj.so.15 \
    && export LD_LIBRARY_PATH=/lib:/usr/lib:/usr/local/lib \
    && python -m pip install -U pip \
    && pip install -r requirements.txt --no-input --no-cache \
    && rm -rf /var/lib/apt/lists/* 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



COPY backend /webapp/backend
RUN  pip install -e /webapp/backend --no-cache
RUN chmod +x ./entrypoint.sh

COPY --from=Client /webapp/backend/templates/base-vue.html /webapp/backend/templates/base-vue.html
COPY --from=Client /webapp/backend/static /webapp/backend/static
RUN ls -R /webapp/backend/static && chmod -R 777 /webapp/backend/static

WORKDIR /webapp/modules
COPY modules .
RUN pip install -e /webapp/modules/geotools
EXPOSE 8000
ENTRYPOINT ["/webapp/backend/entrypoint.sh"]

FROM nginx:stable-alpine as nginx
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=Client /webapp/backend/static /usr/share/nginx/html/static
EXPOSE 8081
