#!/bin/bash
docker compose --file docker-compose-dev.yml --env-file .env-dev down
docker compose --file docker-compose-dev.yml --env-file .env-dev up -d --build