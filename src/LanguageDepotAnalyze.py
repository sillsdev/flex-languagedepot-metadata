#!/usr/bin/python
import sys
import os
import flexdb
from subprocess import check_output
from pipes import quote

class Runner(object):
    """find the files in this directory and ones above this directory, including the mercurial files"""
    def __init__(?, config):
        # currently, we can get the folder we need by where the file was launched from
        global rootProjectFolder
        rootProjectFolder = os.getcwd()

    def run():
        listOfProjects = []
        for root, dirs, files in os.walk(rootProjectFolder):
            # adds directories to the list
            for name in dirs:
                if #check for legitimacy:
                    listOfProjects.append(name)
            # does something for each file in the list, possibly could be used for scanning functions in the future
            #for files in dir:

        for folder in listOfProjects:
            analyzer = Analyze(folder)
            analyzer.analyze()


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

    def analyze():
        self.projectCode = self.name
        self.size = self._getSizeInMB()
        self.numberOfRevisions = self._getNumberOfRevisions()
        self.createdDate = self._getCreatedDate()
        self.modifiedDate = self._getModifiedDate()
        _insertIntoDb()

    # the standard command for getting folder size is filtered down to the mere number
    def _getSizeInMB():
        return check_output( 'du -hcs %s | sed "2q;d" | cut -c1-2' % quote(self.hgdir), shell=True )

    # goes to the folder, gets the tip of the mercurial project, and filters out its commit number
    def _getNumberOfRevisions():
        return check_output( 'cd %s && hg tip --T "{rev}\n"' % quote(self.hgdir), shell=True )

    # goes to the folder, gets the first commit, and filters out the date
    def _getCreatedDate():
        return check_output( 'cd %s && hg log -r 1 --template "{date|shortdate}\n"' % quote(self.hgdir), shell=True)

    # goes to the folder, gets the tip, and filters out the date
    def _getModifiedDate():
        return check_output( 'cd %s && hg tip --template "{date|shortdate}\n"' % quote(self.hgdir), shell=True)

    def _insertIntoDb():
        flexdb.connect()
        flexdb.addItems(self.name, self.projectCode, self.size, self.numberOfRevisions, self.createdDate, self. modifiedDate)
        flexdb.commit()

    # end of Analyze class

if __name__ == '__main__':
    runner = Runner(sys.argv[1], sys.argv[2])
    runner.run()
