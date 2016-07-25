# using a user with createdb and dropdb roles, or the user postgres
echo Emptying languagedepot-metadata database
dropdb languagedepot-metadata --if-exists
createdb languagedepot-metadata
python3 createDb.py
psql languagedepot-metadata < languagedepot-metadata.sql
echo Done
