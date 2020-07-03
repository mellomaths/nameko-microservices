#!/bin/bash

echo "$(date) - Check if rabbit and postgres are up and running before starting the service."

while ! nc -z $RABBIT_HOST $RABBIT_PORT
do 
  echo "$(date) - waiting for rabbitmq..."
  sleep 3
done 

echo "$(date) - Rabbit is up and running."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT
do 
  echo "$(date) - waiting for postgres..."
  sleep 3
done 

echo "$(date) - Postgres is up and running."

# Run Migrations

alembic upgrade head

# Run the service

nameko run --config config.yml orders.service --backdoor 3000