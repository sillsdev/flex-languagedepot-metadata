#!/bin/bash
set -eux

if [ "$#" -ne 2 ]; then
    echo "Usage: ./runAll.sh <directory with projects to scan> <output CSV file>"
    exit 1
fi

# Run everything necessary to get an output file in one command

ORIGINAL_CWD=`pwd`

# cd to the directory of this script
cd "$(dirname "$0")" || exit

./installDependencies.sh --quiet || exit
./setupPostgresql.sh || exit
./createDb.sh || exit
./runAnalysis.py $1 || exit

DIR=`pwd`

# Go back to the original CWD so the file will be saved in the right place

cd $ORIGINAL_CWD || exit

exec "$DIR/saveAsCSV.sh" $2
