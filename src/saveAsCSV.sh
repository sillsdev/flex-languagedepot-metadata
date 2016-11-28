# makes a csv
echo Exporting table project.metadata to file export.csv
psql languagedepot-metadata -c "\copy (SELECT * FROM project.metadata ORDER BY id) TO STDOUT WITH CSV HEADER" > export.csv
