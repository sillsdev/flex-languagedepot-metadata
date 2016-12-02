#!/bin/bash
cd "$(dirname "$0")" || exit

echo "Setting up a database user."
echo "You may be prompted for the password for the $(whoami) user."
echo "As you type the password no output will be shown."
echo

sudo -u postgres psql -c "CREATE ROLE $USERNAME WITH LOGIN CREATEDB PASSWORD 'placeholder'" 2> /dev/null

# Replaces "USERNAME" with the actual username in config.json
sed -i "s/USERNAME/$USERNAME/" config.json

echo Finished
