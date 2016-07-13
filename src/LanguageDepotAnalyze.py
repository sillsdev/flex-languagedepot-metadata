#!/usr/bin/python
import sys
import os
import glob,os.path
import flexdb
from subprocess import check_output
from pipes import quote

class Runner(object):
    """find the files in this directory and ones above this directory,
    including the mercurial files"""
    def __init__(self, config):
        # currently, we can get the folder we need by where the file was launched from
        # we just need to know what the config is for the program
        global rootProjectFolder
        rootProjectFolder = os.getcwd()

        # gets the config file, checks if they supplied credentials
        configOutput = check_output(['cat', config])
        if not "password=" in configOutput: # "password=" is only one format, perhaps add more formats?
            print ("please supply a user password.")
            return
        # stores the user's password (and other account details, once made)
        global usrpasswd
        for entry in configOutput.split('\n'):
            if "password=" in entry:
                passwdLine = entry.strip()
                usrpasswd = passwdLine.replace('password=', '')

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
