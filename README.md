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

- Download the script with `git clone https://github.com/sillsdev/flex-languagedepot-metadata`
- Run the script in `src/runAll.sh`

By default the script will run on the sample data and save the output to `export.csv`. To run on a different dataset pass the path to the directory containing the projects you want to analyze. For example:
```
src/runAll.sh path/to/directory/containing/flex/projects output_file.csv
```
Both parameters are optional, but you must specify the first if you want to specify the second.

### Longer setup

- `cd src`
- run `./installDependencies.sh` to automate installing the above dependencies with apt-get.
- run `./setupPostgresql.sh` to automate creating a role for the database we'll use.
- run `./createDb.sh` to initialize the database, or delete and recreate it.
- run `./runAnalysis.py` to start analyzing the data. You can specify a path to the directory containing the projects you want to analyze.
- run `./saveAsCSV.sh` to export the data from the database. You can specify a file name to save the data in.

### Detailed Setup

The first step is to set up a PostgreSQL user with permissions to add and remove databases. `setupPostgresql.sh` will do this for you, using credentials from the account currently signed in. If you wish to create the account yourself, however, that is also perfectly fine.

The next step is to create a configuration file. Place the following tokens in the file:
```
{
"host":"localhost", // must not be changed
"dbname":"languagedepot-metadata", // can be changed, however, you cannot run 'createdb.sh' on other databases
"username":"postgres",
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
This file will create the database, removing it first if it already exists.

### Usage

in the `src` folder, run `runAnalysis.py`:
```
$ ./runAnalysis.py
```
Your output may look like this:
```
(2/3): Scanning my-flex-project.......Done!
```
If your project only has an initial commit, you may get some extra output from the shell:
```
abort: unknown revision '1'!
(3/3): Scanning another-flex.......Done!
```
However, your data will still be added to the database.

You can now query the database for your project data, with a simple `SELECT * FROM project.metadata;`:
```
$ psql languagedepot-metadata
=# SELECT * FROM project.metadata;
```
However, you can also export the data to a CSV file:
```
=# \copy (SELECT * FROM project.metadata) TO 'data.csv' CSV HEADER;
```
Or just run `./saveAsCSV.sh` to export data to `export.csv`.
