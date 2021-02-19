#!/usr/bin/env python3

# Create files with the flag hash as the file name in the same directory as
# this script and they will be submitted when the script is run.

from os import listdir
from os.path import isfile, join, dirname, abspath
import swpag_client as sc

url='http://TBD'
token= 'TBD'
t = sc.Team(url, token); 
path = dirname(abspath(__file__))
files = [file for file in listdir(path) if isfile(join(path, file))]

for filename in files:
    print(t.submit_flag([filename]))
