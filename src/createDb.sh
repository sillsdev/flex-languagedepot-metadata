#!/bin/bash
set -eux

# cd to the directory of this script
cd "$(dirname "$0")" || exit

# using a user with createdb and dropdb roles, or the user postgres
echo "Emptying the languagedepot-metadata database."

dropdb languagedepot-metadata --if-exists
createdb languagedepot-metadata

python3 createDb.py
psql languagedepot-metadata < languagedepot-metadata.sql

echo Database created
