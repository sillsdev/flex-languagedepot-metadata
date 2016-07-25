#!/bin/bash
DIR=`dirname "$(readlink -f $0)"`

sudo -u postgres psql -c "CREATE ROLE $USERNAME WITH LOGIN CREATEDB PASSWORD 'placeholder'" 2> /dev/null
createdb $USERNAME
sed -i "s/USERNAME/$USERNAME/" $DIR/config.json
