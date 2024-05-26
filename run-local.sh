#!/bin/bash

# The script will prepare the app to run locally by setting the key to the
# correct environment variable.

export GOOGLE_APPLICATION_CREDENTIALS=./key.json
docker-compose up
