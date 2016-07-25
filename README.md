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

- run src/getDependences.sh to automate installing the above dependencies with apt-get
- run src/setupPostgresql.sh to automate creating a role for the database we'll use
- run src/createDb.sh to initialize the database
- run src/runAnalysis.py to start analyzing the data

Note: make sure you have set up your `postgres` user with a database usage password. By default, it will not have a password, and you will need to do this before proceeding. You will also need to be running a user with `createdb` and `dropdb` permissions in postgresql; `postgres` will have these already.

Place all the folders you wish to scan in a single directory. Make a config file with the token 'password', which contains your user password for `postgres`. You may place the config file wherever you like.

Download (or clone) the repository to any given folder. Once done, move to the `src` directory, and open `runAnalysis.py` in a text editor. Replace the variables `cfgName` and `dataPath` with the full paths to your configuration file and data folder, respectively:
```python
cfgName = '/path/to/the/config.json'
dataPath = '/path/to/the/project/folders'
```
run `createDb.sh`:
```
$ ./createDb.sh
```
This file can both create the database and remove previously made ones with the same name.

### Usage

in the `src` folder, run `runAnalysis.py`:
```
$ ./runAnalysis.py
```
If your project has only an initial commit, you may get some output from the shell:
```
abort: unknown revision '1'!
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
