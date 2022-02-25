#!/bin/bash
export DATABASE_URL="heroku-postgresql"
export EXCITED="true"
export DATABASE_URL_test="postgresql://postgres:1@localhost:5432/casting_agency_test"
echo "setup.sh script executed successfully!"