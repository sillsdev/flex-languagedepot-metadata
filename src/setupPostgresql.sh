#!/bin/bash

sudo -u postgres psql -c "CREATE ROLE $USERNAME WITH LOGIN CREATEDB PASSWORD 'placeholder'" 2> /dev/null
createdb $USERNAME
