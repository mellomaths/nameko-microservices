#!/bin/bash

# Check if rabbit and redis are up and running before starting the service.

# until nc -z ${RABBIT_HOST} ${RABBIT_PORT}; do
#     echo "$(date) - waiting for rabbitmq..."
#     sleep 2
# done

# Run Migrations

alembic upgrade head

# Run the service

nameko run --config config.yml orders.service --backdoor 3000