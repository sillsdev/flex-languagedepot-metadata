#!/usr/bin/python
import sys
import os
import glob,os.path # used for finding files/folders
import flexdb
from subprocess import check_output # used for bash commands (when required), unix-only
from pipes import quote # used to sanitize bash input when complex commands are required, unix-only
import json # data type no.1
import yaml # data type no.2, note: LibYAML based. LibYAML makes PyYAML faster.

class Runner(object):
    """find the files in this directory and ones above this directory,
    including the mercurial files"""

    def __init__(self, config):
        # currently, we can get the folder we need by where the file was launched from
        # we just need to know what the config is for the program
        global rootProjectFolder
        rootProjectFolder = os.getcwd()
        self._checkCfgType(config)

        # end of init

    def run(self):
        # find all files/folders in root folder
        files = glob.glob('*')
        listOfProjects = filter(lambda f: os.path.isdir(f), files)
        listOfProjects.sort()
        print (listOfProjects)

        for folder in listOfProjects:
            analyzer = Analyze(folder)
            analyzer.analyze()
            analyzer.insertIntoDb(usrpasswd)

    def _checkCfgType(self, config):
        # declare credential fields here
        global usrpasswd
        # check what kind of format the config file uses
        configOutput = check_output(['cat', config])
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
                else:
                    usrpasswd = parsedConfig['password']

        else:
            # plain text files
            if not "password=" in configOutput: # "password=" is only one format, perhaps add more formats?
                print ('please supply a user password.')
                return
            # stores the user's password (and other account details, once made)
            for entry in configOutput.split('\n'):
                if "password=" in entry:
                    passwdLine = entry.strip()
                    usrpasswd = passwdLine.replace('password=', '')

        # end of _checkCfgType

    # end of Runner class

class Analyze(object):
    """retrieve various valuable pieces of information"""
    # subprocess.check_output() is used because it's a safer format than os.system()
    def __init__(self, hgdir):
        # input folder will be the project name
        self.name = hgdir
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
        return int( (check_output( 'du -hcs %s | sed "2q;d"' % quote(self.hgdir), shell=True )).strip('M\ttotal\n') )

    # goes to the folder, gets the tip of the mercurial project, and filters out its commit number
    def _getNumberOfRevisions(self):
        return int( check_output( 'cd %s && hg tip --template "{rev}"' % quote(self.hgdir), shell=True ) )

    # goes to the folder, gets the first commit, and filters out the date
    def _getCreatedDate(self):
        return check_output( 'cd %s && hg log -r 1 --template "{date|shortdate}"' % quote(self.hgdir), shell=True)

    # goes to the folder, gets the tip, and filters out the date
    def _getModifiedDate(self):
        return check_output( 'cd %s && hg tip --template "{date|shortdate}"' % quote(self.hgdir), shell=True)

    def insertIntoDb(self, passwd):
        flexdb.connect(passwd)
        flexdb.addItems(self.name, self.projectCode, self.size, self.numberOfRevisions, self.createdDate, self. modifiedDate)
        #flexdb.commit()

    # end of Analyze class

if __name__ == '__main__':
    runner = Runner(sys.argv[1])
    runner.run()
