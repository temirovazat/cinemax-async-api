#!/bin/bash
elastic_ready() {
    $(which curl) -s http://${ELASTIC_HOST:-localhost}:${ELASTIC_PORT:-9200} >/dev/null 2>&1
}

redis_ready() {
    exec 3<>/dev/tcp/${REDIS_HOST:-localhost}/${REDIS_PORT:-6379} && echo -e "PING\r\n" >&3 && head -c 7 <&3 | grep 'PONG'
}

until redis_ready; do
  >&2 echo 'Waiting for Redis to become available...'
  sleep 1
done
>&2 echo 'Redis is available.'

until elastic_ready; do
  >&2 echo 'Waiting for Elasticsearch to become available...'
  sleep 1
done
>&2 echo 'Elasticsearch is available.'

gunicorn main:app --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker