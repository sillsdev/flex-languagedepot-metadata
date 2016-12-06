#!/bin/bash
cd "$(dirname "$0")" || exit

function createRole {
  echo "Setting up a database user."
  echo "You may be prompted for the password for the $USERNAME user."
  echo "As you type the password no output will be shown."
  echo
  sudo -u postgres psql -c "CREATE ROLE $USERNAME WITH LOGIN CREATEDB PASSWORD 'placeholder'"
}

# If There is no Postgre role with the username, create it
[ $(psql postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$USERNAME'") != "1" ] && createRole

# Replaces "USERNAME" with the actual username in config.json
sed -i "s/USERNAME/$USERNAME/" config.json

echo "Postgre setup done"
