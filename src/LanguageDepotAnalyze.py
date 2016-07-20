#!/usr/bin/python3
import sys
import os
import glob
import json # data type no.1
import yaml # data type no.2, note: LibYAML based. LibYAML makes PyYAML faster at the cost of being C-based.
import psycopg2
from importlib import import_module
import subprocess
from pipes import quote

class Runner(object):
    """find the files in this directory and ones above this directory,
    including the mercurial files"""

    def __init__(self, config, dataPath):
        # makes sure the data path is correctly formatted (last character must contain '/')
        global rootProjectFolder
        if (dataPath[len(dataPath)-1:] == "/"):
            rootProjectFolder = dataPath
        else:
            rootProjectFolder = dataPath + '/'

        self._checkCfgType(config)

        # end of init


    def _checkCfgType(self, config):
        # declare credential fields here
        global usrpasswd
        # check what kind of format the config file uses
        configOutput = subprocess.check_output(['cat', config])

        # JSON
        if ( ".json" in config ):
            try:
                parsedConfig = json.loads(configOutput)
                parsedConfig['password']
            except (ValueError):
                print ("%s is not valid json.") % (config)
                return
            except (KeyError):
                print ("%s does not contain proper credentials. (must include 'password')") % (config)
            else:
                usrpasswd = parsedConfig['password']
        # Yaml Ain't Markup Language (but it is pretty good object notation)
        elif( ".yaml" in config or ".yml" in config ):
            try:
                parsedConfig = yaml.safe_load(configOutput)
                parsedConfig['password']
            except (yaml.scanner.ScannerError):
                print ("%s is not valid. (might contain tabs in entries)") % (config)
            else:
                if ( parsedConfig['password'] == None ):
                    print ('please supply a user password.')
                    return
                else:
                    usrpasswd = parsedConfig['password']
        # plain text files
        else:
            if ( not "password=" in configOutput ): # "password=" is only one format, perhaps add more formats?
                print ('please supply a user password.')
                return
            # stores the user's password (and other account details, once made)
            for entry in configOutput.split('\n'):
                if "password=" in entry:
                    passwdLine = entry.strip()
                    usrpasswd = passwdLine.replace('password=', '')

        # end of _checkCfgType

    def run(self):
        # checks to see if the credentials came through
        if ( not "usrpasswd" in globals() ):
            print ('Not enough credentials.')
            return
        # find all files/folders in root folder
        files = glob.glob(rootProjectFolder + '*')
        files.sort()
        listOfProjects = filter(lambda f: os.path.isdir(f), files)
        # print (listOfProjects)

        for folder in listOfProjects:
            # Analyzer needs to pass rootProjectFolder as a parameter
            # so that the directory can be cropped out of the name later
            analyzer = Analyze(folder, rootProjectFolder)
            analyzer.run(usrpasswd)

    # end of Runner class



class Analyze(object):
    """retrieve various valuable pieces of information"""
    def __init__(self, hgdir, parentDirs):
        # to get the project name, we take the complete directory sans the parent directories
        self.name = hgdir[len(parentDirs):]
        self.hgdir = hgdir

    def run(self, password):
        # make connection to database
        conn_string = 'host=localhost dbname=languagedepot-metadata user=postgres password=' + password
        try:
            conn = psycopg2.connect(conn_string)
        except:
            print('Incorrect Credentials.')
            return

        # insert name into database, this creates a row we can use later
        curs = conn.cursor()
        curs.execute( "INSERT INTO project.metadata (name) VALUES (%s);", (self.name,) )

        listOfCapabilities = self.getListOfCapabilities()
        # import a capability module from the list
        # use a capability to get data from the project, then add that data
        # to the row received from before
        for capabilityName in listOfCapabilities:
            capabilityModule = import_module(capabilityName)
            result = capabilityModule.tasks.analyze(self.hgdir)
            capabilityModule.tasks.updateDb(conn_string, self.name, result)

    def getListOfCapabilities(self):
        # glob all classes in the capabilities folder
        # except the base class (capability.py) and __init__.py
        listOfCapabilities = []
        unfiltered = glob.glob('capabilities/*.py')
        unfiltered.remove('capabilities/capability.py')
        unfiltered.remove('capabilities/__init__.py')
        for item in unfiltered:
            listOfCapabilities.append(item.replace('/', '.').replace('.py', ''))
        return listOfCapabilities

    # end of Analyze class
