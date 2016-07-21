#!/usr/bin/python3
import os
from LanguageDepotAnalyze import Runner

# config file is specified, then used for the program!
cfgName = '/home/daniel/git/flex-languagedepot-metadata/src/exConfig.json'
dataPath = '/home/daniel/git/flex-languagedepot-metadata/data'
runner = Runner(cfgName, dataPath)
runner.run()
