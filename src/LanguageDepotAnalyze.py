#!/usr/bin/python3
import sys
import traceback
import os
import glob
import json  # data type no.1
import psycopg2
from importlib import import_module
import subprocess


class Runner(object):
    """find the files in this directory and ones above this directory,
    including the mercurial files"""

    def __init__(self, config, dataPath):
        # Makes sure dataPath ends with a '/' character
        global rootProjectFolder
        if (dataPath[-1] == "/"):
            rootProjectFolder = dataPath
        else:
            rootProjectFolder = dataPath + '/'

        self._checkCfgType(config)

        # end of init

    def _checkCfgType(self, config):
        # declare credential fields here
        global usrhost
        global databse
        global usrname
        global usrpasswd
        # check what kind of format the config file uses
        configOutput = subprocess.check_output(['cat', config]).decode('utf-8')
        try:
            parsedConfig = json.loads(configOutput)
            parsedConfig['host']
            parsedConfig['dbname']
            parsedConfig['user']
            parsedConfig['password']
        except (ValueError):
            print("{} is not valid json.".format(config))
            return
        except (KeyError):
            print("{} does not contain proper credentials. "
                  "(must include 'host', 'dbname', 'user', and 'password')"
                  .format(config))
            return
        else:
            usrhost = parsedConfig['host']
            databse = parsedConfig['dbname']
            usrname = parsedConfig['user']
            usrpasswd = parsedConfig['password']

    def run(self):
        # checks to see if the credentials came through
        if (
            "usrpasswd" not in globals() or
            "usrname" not in globals() or
            "databse" not in globals() or
            "usrhost" not in globals()
        ):
            print('Not enough credentials.')
            return
        # now it connects to the database, to see if they're correct
        conn_string = 'host={} dbname={} user={} password={}'.format(
                      usrhost, databse, usrname, usrpasswd)
        try:
            conn = psycopg2.connect(conn_string)
        except Exception:
            print('Incorrect Credentials.')
            raise Exception

        # find all files/folders in root folder
        files = glob.glob(rootProjectFolder + '*')
        files.sort()
        listOfProjects = [f for f in files if os.path.isdir(f)]
        numOfProjects = len(listOfProjects)

        for folder in listOfProjects:
            fldrIndex = listOfProjects.index(folder)
            # Analyzer needs to pass rootProjectFolder as a parameter
            # so that the directory can be cropped out of the name later
            analyzer = Analyze(
                folder, rootProjectFolder, fldrIndex, numOfProjects)
            try:
                analyzer.run(conn)
            except Exception:
                print("Unfortunately, %s had a problem:\n" % folder)
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print("-"*60)
                print("Moving on...\n\n")

    # end of Runner class


class Analyze(object):
    """retrieve various valuable pieces of information"""
    def __init__(self, hgdir, parentDirs, current, totalNumber):
        # To get the project name, remove the parent directories from the
        # project's path to get just the directory name.
        self.name = hgdir[len(parentDirs):]
        self.hgdir = hgdir
        print(
            '(%s/%s) Scanning %s' % (current+1, totalNumber, self.name),
            end='')

    def run(self, conn):
        # check if the project is already entered into the database, otherwise
        # continue as normal
        # Why? In what situation would it be scanned twice? XXX
        curs = conn.cursor()
        curs.execute(
            "SELECT scanDone FROM project.metadata WHERE name = %s;",
            (self.name,))

        entries = curs.fetchone()
        if (entries == (True,)):
            print('\nAlready scanned. Moving on...')
            return
        else:
            # insert name into database, this creates a row we can use later
            curs.execute(
                "INSERT INTO project.metadata (name) VALUES (%s);",
                (self.name,))

            curs.execute(
                "UPDATE project.metadata SET projectCode = %s "
                "WHERE name = %s;",
                (self.name, self.name))
            conn.commit()

            listOfCapabilities = getListOfCapabilities()
            # import a capability module from the list
            # use a capability to get data from the project, then add that data
            # to the row received from before
            for capabilityName in listOfCapabilities:
                capabilityModule = import_module(capabilityName)
                print('.', end='')
                result = capabilityModule.tasks.analyze(self.hgdir)
                capabilityModule.tasks.updateDb(conn, self.name, result)

            # Set scanDone to True in the database
            curs.execute(
                "UPDATE project.metadata SET scanDone = %s WHERE name = %s;",
                (True, self.name))
            conn.commit()
            print('Done!')

        # end of run()

    # end of Analyze class


def getListOfCapabilities():
    # glob all classes in the capabilities folder
    # except the base class (capability.py) and __init__.py
    listOfCapabilities = []
    unfiltered = glob.glob('capabilities/*.py')
    unfiltered.remove('capabilities/capability.py')
    unfiltered.remove('capabilities/__init__.py')
    for item in unfiltered:
        listOfCapabilities.append(item.replace('/', '.').replace('.py', ''))
    return listOfCapabilities
