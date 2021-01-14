ARG PYTHON_IMAGE="python:3.9.1-alpine3.12"
ARG NODE_IMAGE="node:14.15.4-alpine3.12"

ARG BUILD_DATE
ARG GIT_HASH
ARG VERSION
ARG VUE_APP_OIDC_AUTHORITY
ARG VUE_APP_OIDC_CLIENTID

FROM $PYTHON_IMAGE AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV STATIC_ROOT /venv/static/static

RUN     apk add --no-cache --virtual build-dependencies \
            build-base \
            libffi-dev \
            postgresql-dev

COPY    requirements.txt /

RUN     pip install virtualenv && \
            virtualenv /venv && \
            source /venv/bin/activate && \
            pip install -r /requirements.txt

COPY    . /venv/aws_tools_proj
WORKDIR /venv/aws_tools_proj
RUN     DJANGO_SETTINGS_MODULE="aws_backup_proj.base_settings" /venv/bin/python manage.py collectstatic --noinput --clear


FROM node:14.10.1-alpine3.12 AS node-builder

ARG VERSION
ARG VUE_APP_OIDC_AUTHORITY
ARG VUE_APP_OIDC_CLIENTID

COPY ./aws_tools/frontend /venv/frontend/
WORKDIR /venv/frontend
RUN npm install
RUN env VUE_APP_VERSION=$VERSION VUE_APP_OIDC_AUTHORITY=$VUE_APP_OIDC_AUTHORITY VUE_APP_OIDC_CLIENTID=$VUE_APP_OIDC_CLIENTID npm run build


FROM $PYTHON_IMAGE

ARG     VERSION
ARG     BUILD_DATE
ARG     GIT_HASH

LABEL org.opencontainers.image.version="$VERSION"
LABEL org.opencontainers.image.created="$BUILD_DATE"
LABEL org.opencontainers.image.revision="$GIT_HASH"
LABEL org.opencontainers.image.title="AWS Tools"
LABEL org.opencontainers.image.description="Tools to help with AWS operations"
LABEL org.opencontainers.image.vendor="Vlad Vasiliu"
LABEL org.opencontainers.image.source="https://github.com/vladvasiliu/aws_tools"
LABEL org.opencontainers.image.authors="Vlad Vasiliu"
LABEL org.opencontainers.image.url="https://github.com/vladvasiliu/aws_tools"

EXPOSE 8001

RUN     apk add --no-cache libpq

COPY --from=builder /venv /venv
COPY --from=node-builder /venv/frontend/dist /venv/static
VOLUME /venv/static
WORKDIR /venv/aws_tools_proj
