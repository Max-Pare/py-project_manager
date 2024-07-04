import pathlib
import re
import os
import json
import glob
import threading
import multiprocessing
import numpy as np


PY_PROJMAN_CONFIG_DIR = './.ppm_config/'
PY_PROJMAN_CACHE = PY_PROJMAN_CONFIG_DIR + '.ppmcache.json'
PY_PROJMAN_SETTINGS = PY_PROJMAN_CONFIG_DIR + '.ppmconfig.json'

CPU_COUNT = multiprocessing.cpu_count()

DEFAULT_CONFIG = {'entry': 'Not much to see here yet.'}

if not os.path.isdir(PY_PROJMAN_CONFIG_DIR):
    os.mkdir(PY_PROJMAN_CONFIG_DIR)
if not os.path.isfile(PY_PROJMAN_SETTINGS):
    with open(PY_PROJMAN_SETTINGS, 'w') as file:
        json.dump(DEFAULT_CONFIG, file)
if not os.path.isfile(PY_PROJMAN_CACHE):
    with open(PY_PROJMAN_CACHE, 'w') as file:
        json.dump(set([]), file)

try:
    with open(PY_PROJMAN_CACHE, 'r') as file:
        cache = set(json.load(file))
except FileNotFoundError as e:
    print(f'Cache file not found at "{PY_PROJMAN_CACHE}"!!!')
    print(e)
    exit(-1)
if not cache and input('Scan current folder for existing projects? (y/n):').lower() == 'y':
    dirs = set(glob.iglob('./**'))
    for dir in dirs:
        if not os.path.isdir(dir): continue
        cache.add(pathlib.Path(dir).name)
    with open(PY_PROJMAN_CACHE, 'w') as file:
        file.write('\n'.join(cache))
print(*cache, sep='\n')        
# thall