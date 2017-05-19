#!/usr/bin/python3
from LanguageDepotAnalyze import getListOfCapabilities
from importlib import import_module
# in this file, we write a SQL script which will create the database.
# the script will take this format:
#
# -- create schemas
# CREATE SCHEMA project;
#
# -- set search path
# SET search_path TO project,public;
#
# -- create tables
# CREATE TABLE project.metadata (
# name              varchar(80),
# id                serial,
# projectCode       varchar(80), -- same as name
# projectSizeInMB   int,
# numberOfRevisions int,
# createdDate       date, -- Date of first commit
# modifiedDate      date -- Date of last commit
# );


def main():
    # Here, we make the list of elements. The first three added here are
    # non-capabilites and MUST NOT be removed. Removing the element 'name' will
    # break the program entirely.
    listOfElements = []
    listOfElements.append(['name', 'varchar(80)'])
    listOfElements.append(['id', 'serial'])
    listOfElements.append(['projectCode', 'varchar(80)'])
    # Using the list of capabilities, we import each capability and use its
    # getColumns() function to add it to the list of elements.
    # If the list contains a list, then we add in the metalist as if it were a
    # column.
    # All other metalists in the list are added in the same way.
    listOfCapabilities = getListOfCapabilities()
    for capability in listOfCapabilities:
        capabilityModule = import_module(capability)
        if isinstance(capabilityModule.tasks.getColumns()[0], list):
            for element in capabilityModule.tasks.getColumns():
                if len(element) % 2 == 0:
                    listOfElements.append(element)
                else:
                    raise ValueError('please insert a type for each element.')
        elif len(capabilityModule.tasks.getColumns()) % 2 == 0:
            listOfElements.append(capabilityModule.tasks.getColumns())
        else:
            raise ValueError('please insert a type for each element.')
    # this element must be last, it tells the program if the file is done
    # scanning
    listOfElements.append(['scanDone', 'boolean'])

    # SQL string variables
    schema = ['-- create schemas\n',
              'CREATE SCHEMA project;\n',
              '-- set search path\n',
              'SET search_path TO project,public;\n'
              ]
    tableStart = ['-- create tables\n',
                  'CREATE TABLE project.metadata (\n'
                  ]
    tableEnd = ');\n'

    # write!
    sqlFile = open('languagedepot-metadata.sql', 'w')
    sqlFile.writelines(schema)
    sqlFile.writelines(tableStart)
    for element in listOfElements:
        # If it's the very last element
        if element == listOfElements[-1]:
            sqlFile.write(element[0] + ' ' + element[1] + '\n')
        else:
            sqlFile.write(element[0] + ' ' + element[1] + ',' + '\n')
    sqlFile.write(tableEnd)
    sqlFile.close()

    # end of main()


if __name__ == "__main__":
    main()
