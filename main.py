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


def main():
    cache, config = setup()


def setup() -> tuple[set, dict]:
    work_dir = None
    config = None
    # TODO: should make file existence checks more consistent, either try: open or if exists: .
    if not os.path.isdir(PY_PROJMAN_CONFIG_DIR):
        os.mkdir(PY_PROJMAN_CONFIG_DIR)
    if not os.path.isfile(PY_PROJMAN_SETTINGS):
        with open(PY_PROJMAN_SETTINGS, 'w') as file:
            json.dump(DEFAULT_CONFIG, file)
    if not os.path.isfile(PY_PROJMAN_CACHE):
        with open(PY_PROJMAN_CACHE, 'w') as file:
            json.dump(list(), file)
    try:
        with open(PY_PROJMAN_CACHE, 'r') as file:
            cache = set(json.load(file))
    except FileNotFoundError as e:
        print(f'Cache file not found at "{PY_PROJMAN_CACHE}"!!!\n' + str(e))
        exit(-1)
    try:
        with open(PY_PROJMAN_SETTINGS, 'r') as file:
            config = dict(json.load(file))
    except FileNotFoundError as e:
        print(f'Config file not found at "{PY_PROJMAN_SETTINGS}"!!!\n' + str(e))
        exit(-1)
    if work_dir := config.get('work_dir') is None:
        _raw_input = input('Enter the parent directory of your projects: ').strip()
        if os.path.isdir(_raw_input):
            work_dir = _raw_input
    if not cache and input('Scan current folder for existing projects? (y/n):').lower() == 'y':
        dirs = set(glob.iglob(f'{work_dir}/**'))
        for dir in dirs:
            if not os.path.isdir(dir): continue
            cache.add(pathlib.Path(dir).name)
        with open(PY_PROJMAN_CACHE, 'w') as file:
            file.write('\n'.join(cache))
    print(*cache, sep='\n')
    return cache, config


if __name__ == '__main__':
    main()

# thall
