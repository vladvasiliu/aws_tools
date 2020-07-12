FROM python:3.8.3-alpine3.12 AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV STATIC_ROOT /venv/static/static

RUN     apk add --no-cache --virtual build-dependencies \
            build-base \
            libffi-dev \
            postgresql-dev

COPY    aws_tools/requirements.txt /

RUN     pip install virtualenv && \
            virtualenv /venv && \
            source /venv/bin/activate && \
            pip install -r /requirements.txt

COPY    . /venv/aws_tools_proj
WORKDIR /venv/aws_tools_proj
RUN     DJANGO_SETTINGS_MODULE="aws_backup_proj.base_settings" /venv/bin/python manage.py collectstatic --noinput --clear


FROM node:lts-alpine AS node-builder

ARG VERSION
ARG VUE_APP_OIDC_AUTHORITY
ARG VUE_APP_OIDC_CLIENTID

COPY ./aws_tools/frontend /venv/frontend/
WORKDIR /venv/frontend
RUN npm install
RUN env VUE_APP_VERSION=$VERSION VUE_APP_OIDC_AUTHORITY=$VUE_APP_OIDC_AUTHORITY VUE_APP_OIDC_CLIENTID=$VUE_APP_OIDC_CLIENTID npm run build


FROM python:3.8.3-alpine3.12

LABEL description="AWS Tools"
LABEL maintainer="Vlad Vasiliu <vladvasiliun@yahoo.fr>"

EXPOSE 8001

RUN     apk add --no-cache libpq

COPY --from=builder /venv /venv
COPY --from=node-builder /venv/frontend/dist /venv/static
VOLUME /venv/static
WORKDIR /venv/aws_tools_proj
