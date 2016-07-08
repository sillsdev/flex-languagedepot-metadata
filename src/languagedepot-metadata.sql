-- create schemas
CREATE SCHEMA project;

-- set search path
SET search_path TO project,public;

-- create tables
CREATE TABLE project.metadata (
name				      varchar(80),
id                serial,
projectCode       varchar(80), -- same as name
projectSizeInMB   int,
numberOfRevisions int,
createdDate       date, -- Date of first commit
modifiedDate      date -- Date of last commit
);
