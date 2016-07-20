# makes a csv
echo "\copy (SELECT * FROM project.metadata) TO '/home/daniel/test1.csv' WITH (FORMAT CSV);" | psql languagedepot-metadata
