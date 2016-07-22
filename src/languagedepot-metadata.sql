-- create schemas
CREATE SCHEMA project;
-- set search path
SET search_path TO project,public;
-- create tables
CREATE TABLE project.metadata (
name varchar(80),
id serial,
projectCode varchar(80),
createdDate date,
committerNames text,
committerNumber int,
projectSizeInMB int,
numberOfRevisions int,
modifiedDate date
);
