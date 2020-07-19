#!/bin/bash

if [[ -z "${ENV}" ]]; then
  export GUNICORN_CMD_ARGS="-w 4 -k uvicorn.workers.UvicornWorker"
else
  export GUNICORN_CMD_ARGS="--bind=0.0.0.0 -w 4 -k uvicorn.workers.UvicornWorker"
fi

gunicorn app.main:app