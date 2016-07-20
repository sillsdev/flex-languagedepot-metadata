# makes a csv
psql languagedepot-metadata
\copy (SELECT * FROM project.metadata) TO '/home/daniel/test1.csv' WITH (FORMAT CSV);
\q
