# flex-languagedepot-metadata

A python script to collect FLEx metadata from a list of local project folders and store the data in a relational database for further analysis and query

### Features

* scans multiple folders for project data
* stores data using the PostgreSQL database technology
* independent of directory placement

### Dependencies

* Python 3 (tested with 3.5)
* [PostgreSQL](https://www.postgresql.org/) (tested with 9.4, 9.5)
* [psycopg2](http://initd.org/psycopg/)

### Quickstart

- run `src/getDependences.sh` to automate installing the above dependencies with apt-get
- run `src/setupPostgresql.sh` to automate creating a role for the database we'll use
- run `src/createDb.sh` to initialize the database
- run `src/runAnalysis.py` to start analyzing the data

### Detailed Setup

The first step is to set up a PostgreSQL user with permissions to add and remove databases. `setupPostgresql.sh` will do this for you, using credentials from the account currently signed in. If you wish to create the account yourself, however, that is also perfectly fine.

The next step is to create a configuration file. Place the following tokens in the file:
```json
{
"host":"localhost" # must not be changed
"dbname":"languagedepot-metadata" # can be changed, however, you cannot run 'createdb.sh' on other databases
"username":"postgres"
"password":"placeholder"
}
```
Place the config file wherever you like.

Download (or clone) the repository to any given folder. Once done, move to the `src` directory, and open `runAnalysis.py` in a text editor. Replace the variables `cfgName` and `dataPath` with the full paths to your configuration file and data folder, respectively:
```python
cfgName = '/path/to/the/config.json'
dataPath = '/path/to/the/project/folders'
```
run `createDb.sh`:
```
$ ./createDb.sh
```
This file can both create the database and remove the database if it's already been made.

### Usage

in the `src` folder, run `runAnalysis.py`:
```
$ ./runAnalysis.py
```
Your output may look like this:
```
my-flex-project: Scanning in process
my-flex-project: Scanned!
```
If your project only has an initial commit, you may get some extra output from the shell:
```
another-flex: Scanning in process
abort: unknown revision '1'!
another-flex: Scanned!
```
However, your data will still be added to the database.

You can now query the database for your project data, with a simple `SELECT * FROM project.metadata;`:
```
$ psql languagedepot-metadata
=# SELECT * FROM project.metadata;
```
However, you can also export the data to a CSV file:
```
=# \copy (SELECT * FROM project.metadata) TO '/your/data/goes/here.csv' WITH (FORMAT CSV);
```
