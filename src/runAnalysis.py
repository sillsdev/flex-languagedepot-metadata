#!/usr/bin/python3
import os
from LanguageDepotAnalyze import Runner

# config file is specified, then used for the program!
cfgName = 'config.json'
dataPath = '../data'
runner = Runner(cfgName, dataPath)
runner.run()
