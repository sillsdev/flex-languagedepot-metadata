#!/usr/bin/python
import os
from LanguageDepotAnalyze import Runner

# looks at where the project is placed, and moves to
# the data directory based on that information
dataPath = '/data'
projPath = os.getcwd().replace('/src', '')
os.chdir(projPath + dataPath)

# config file is specified, then used for the program!
cfgName = 'elconfig'
runner = Runner(cfgName)
runner.run()
