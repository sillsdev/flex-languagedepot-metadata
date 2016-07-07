-- create schemas
CREATE SCHEMA project;

-- set search path
SET search_path TO project,public;

-- create tables
CREATE TABLE project.metadata (
name				varchar(80),
id					serial,
projectCode			varchar(80), -- same as name
projectSizeInMB		int,
numberOfRevisions	int,
createdDate			int, -- Date of first commit
modifiedDate		int, -- Date of last commit
);
