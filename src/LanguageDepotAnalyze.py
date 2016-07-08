#!/usr/bin/python
import postflexdb
import os

# find the files in this directory and ones above this directory, including the mercurial files
hgdir = testlangproj-ih-flex

# retrieve various valuable pieces of information
def getName:
    os.command('cd %s && hg tip --template "{node}\n"', % hgdir) # will get the project name eventually

def getSizeInMB:
    os.command('du -hcs %s | sed "2q;d" | cut -c1-2', % hgdir)

def getNumberOfRevisions:
    os.command('cd %s && hg tip --template "{rev}\n"', % hgdir)

def getCreatedDate:
    os.command('cd %s && hg tip --template "{date|shortdate}\n"', % hgdir) # "2006-09-18" sort of date

def getModifiedDate:
    os.command('cd %s && hg tip --template "{node}\n"', % hgdir) # will get the latest commit eventually
