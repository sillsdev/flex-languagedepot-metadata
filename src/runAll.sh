#!/bin/bash

# Run everything necessary to get an output file in one command

ORIGINAL_CWD=`pwd`

# cd to the directory of this script
cd "$(dirname "$0")" || exit

./installDependencies.sh --quiet
./setupPostgresql.sh
./createDb.sh
./runAnalysis.py $1

DIR=`pwd`

# Go back to the original CWD so the file will be saved in the right place

cd $ORIGINAL_CWD || exit

exec "$DIR/saveAsCSV.sh" $2
