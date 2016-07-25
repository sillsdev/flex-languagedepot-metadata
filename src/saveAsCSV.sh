# makes a csv
echo Exporting table project.metadata to file export.csv
psql languagedepot-metadata -c "\copy (SELECT * FROM project.metadata) TO STDOUT WITH (FORMAT CSV)" > export.csv
