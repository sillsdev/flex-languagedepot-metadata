createdb projectDatabase
psql projectDatabase
-- configure the schema
CREATE SCHEMA metadata;
SET search_path TO metadata,public;


-- create the table
CREATE TABLE metadata.project (
name varchar(40), -- determine best length
id varchar(20), -- varchar or another variable type?
projectCode varchar(40), -- same as name
projectSizeInMB numeric,
numberOfRevisions int,
createdDate date, -- first commit
modifiedDate date, -- latest commit
);
\q
