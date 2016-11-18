#!/usr/bin/python3
import sys
from LanguageDepotAnalyze import Runner

# config file is specified, then used for the program!
cfgName = 'config.json'
dataPath = '../data'
if len(sys.argv) == 2:
    dataPath = sys.argv[1]
print("Analyzing directory %s\n" % dataPath)
runner = Runner(cfgName, dataPath)
runner.run()
