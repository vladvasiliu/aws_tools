FROM python:3.8.3-alpine3.12 AS builder

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

FROM python:3.8.3-alpine3.12

LABEL description="AWS Tools"
LABEL maintainer="Vlad Vasiliu <vladvasiliun@yahoo.fr>"

EXPOSE 8001

RUN     apk add --no-cache postgresql-dev

COPY --from=builder /venv /venv
WORKDIR /venv/aws_tools_proj