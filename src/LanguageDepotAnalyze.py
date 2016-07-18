#!/usr/bin/python
import sys
import os
import glob # used for finding files/folders
import flexdb
import subprocess # used for bash commands (when required), unix-only
from pipes import quote # used to sanitize bash input when complex commands are required, unix-only
import json # data type no.1
import yaml # data type no.2, note: LibYAML based. LibYAML makes PyYAML faster at the cost of being C-based.

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
        if ( ".json" in config ):
            # JSON
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
        elif( ".yaml" in config or ".yml" in config ):
            # Yaml Ain't Markup Language (but it is pretty good object notation)
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
        else:
            # plain text files
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
        if ( not 'usrpasswd' in globals() ):
            print "Not enough credentials."
            return
        # find all files/folders in root folder
        files = glob.glob(rootProjectFolder + '*')
        listOfProjects = filter(lambda f: os.path.isdir(f), files)
        listOfProjects.sort()
        # print (listOfProjects)

        for folder in listOfProjects:
            # Analyzer needs to pass rootProjectFolder as a parameter
            # so that the directory can be cropped out of the name later
            analyzer = Analyze(folder, rootProjectFolder)
            analyzer.analyze()
            analyzer.insertIntoDb(usrpasswd)

    # end of Runner class

class Analyze(object):
    """retrieve various valuable pieces of information"""
    # subprocess.check_output() is used because it's a safer format than os.system()
    def __init__(self, hgdir, parentDirs):
        # project name is the complete directory minus anything not the project folder
        self.name = hgdir[len(parentDirs):]
        self.projectCode = None
        self.size = None
        self.numberOfRevisions = None
        self.createdDate = None
        self.modifiedDate = None
        self.hgdir = hgdir

    def analyze(self):
        self.projectCode = self.name
        self.size = self._getSizeInMB()
        self.numberOfRevisions = self._getNumberOfRevisions()
        self.createdDate = self._getCreatedDate()
        self.modifiedDate = self._getModifiedDate()

    # the standard command for getting folder size is filtered down to the mere number
    def _getSizeInMB(self):
        catch = subprocess.check_output( 'du -hcs %s | sed "2q;d"' % quote(self.hgdir), shell=True ).strip('M\ttotal\n')
        if ('K' in catch):
            return 1
        else:
            return int(catch)

    # goes to the folder, gets the tip of the mercurial project, and filters out its commit number
    def _getNumberOfRevisions(self):
        return int( subprocess.check_output( 'cd %s && hg tip --template "{rev}"' % quote(self.hgdir), shell=True ) )

    # goes to the folder, gets the first commit, and filters out the date
    # sometimes the project doesn't have a first commit, so it returns the zeroth commit
    def _getCreatedDate(self):
        try:
            subprocess.check_output( 'cd %s && hg log -r 1 --template "{date|shortdate}"' % quote(self.hgdir), shell=True)
        except(subprocess.CalledProcessError):
            return subprocess.check_output( 'cd %s && hg log -r 0 --template "{date|shortdate}"' % quote(self.hgdir), shell=True)
        else:
            return subprocess.check_output( 'cd %s && hg log -r 1 --template "{date|shortdate}"' % quote(self.hgdir), shell=True)

    # goes to the folder, gets the tip, and filters out the date
    def _getModifiedDate(self):
        return subprocess.check_output( 'cd %s && hg tip --template "{date|shortdate}"' % quote(self.hgdir), shell=True)

    def insertIntoDb(self, passwd):
        flexdb.connect(passwd)
        flexdb.addItems(self.name, self.projectCode, self.size, self.numberOfRevisions, self.createdDate, self. modifiedDate)
        flexdb.commit()

    # end of Analyze class

if __name__ == '__main__':
    runner = Runner(sys.argv[1])
    runner.run()
