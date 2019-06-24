#!/bin/bash
set -eu

# Exports the database to a CSV file. The default file name is export.csv. This
# may be overridden by passing the desired file name as an argument.

OUTPUT=${1:-"export.csv"}

# makes a csv
echo Exporting table project.metadata to file $OUTPUT
psql languagedepot-metadata -c "\copy (SELECT * FROM project.metadata ORDER BY id) TO STDOUT WITH CSV HEADER" > $OUTPUT
