FROM 14.15-buster-slim AS Client
WORKDIR /webapp/frontend
COPY frontend/package.json ./package.json
RUN mkdir -p /webapp/backend/templates
RUN npm install
COPY frontend .
RUN npm run build



FROM 3.8.7-slim-buster AS Django
# set environment variables
# install psycopg2 dependencies
RUN apt update \
    && apt install postgresql-dev gcc python3-dev musl-dev
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /webapp/backend
COPY backend/requirements.txt ./requirements.txt
RUN python -m pip install -U pip \
    pip install -r requirements.txt --no-input

COPY backend .
RUN  pip install -e /webapp/backend
RUN chmod +x ./entrypoint.sh

COPY --from=Client /webapp/backend/templates/base-vue.html /webapp/backend/templates/base-vue.html

WORKDIR /webapp/modules
COPY modules .
RUN pip install -e /webapp/modules/geotools
ENTRYPOINT ["/webapp/backend/entrypoint.sh"]
