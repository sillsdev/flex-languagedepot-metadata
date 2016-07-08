# using user daniel or postgres
dropdb languagedepot-metadata --if-exists
createdb languagedepot-metadata
psql languagedepot-metadata < languagedepot-metadata.sql
