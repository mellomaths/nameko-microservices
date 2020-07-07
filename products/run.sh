#!/bin/bash

echo "$(date) - Check if rabbit and mongodb are up and running before starting the service."

while ! nc -z $RABBIT_HOST $RABBIT_PORT
do
  echo "$(date) - waiting for rabbitmq..."
  sleep 3
done

echo "$(date) - Rabbit is up and running."

while ! nc -z $MONGODB_HOST $MONGODB_PORT
do
  echo "$(date) - waiting for mongodb..."
  sleep 3
done

echo "$(date) - MongoDB is up and running."

# Run the service

nameko run --config config.yml products.service --backdoor 3000