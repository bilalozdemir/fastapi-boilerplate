FROM python:3.7.3-alpine AS base

FROM base AS builder

COPY requirements.txt .

RUN apk add --update gcc musl-dev linux-headers build-base \
    && pip install -r /requirements.txt \
    && apk del musl-dev gcc linux-headers build-base

FROM base AS stage

ENV API_CONFIG ".stage-env"
ENV PORT 8888

COPY --from=builder /usr/local/lib/python3.7 /usr/local/lib/python3.7
COPY . .

EXPOSE $PORT

CMD API_CONFIG=$API_CONFIG python run.py

FROM base AS deployment

ENV API_CONFIG ".env"
ENV PORT 8888

COPY --from=builder /usr/local/lib/python3.7 /usr/local/lib/python3.7
COPY . .

EXPOSE $PORT

CMD API_CONFIG=$API_CONFIG python run.py
