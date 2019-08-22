import sys
import os
import subprocess
import csv

import inifile

lines = [ ['name', 'desc', 'filesize', 'created', 'last_modified'] ]

directory = sys.argv[1]
cwd = os.getcwd()

os.chdir(directory) # for git to function correctly

for filename in os.listdir(directory):    
    pathedname = os.path.join(directory, filename)
    ini = inifile.IniFile(pathedname)

    name = filename    
    desc = ini.get('vars.desc', 'DESC-TODO')
    filesize = ini.get('vars.filesize')
    created = subprocess.Popen(f'git log --follow --format=%aD {pathedname} | tail -1', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip()
    last_modified = subprocess.Popen(f'git log --follow --format=%aD {pathedname} | head -1', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip()

    lines.append([ name, desc, filesize, created, last_modified])

os.chdir(cwd) # save csv to old cwd
with open('pages/pkgs.csv', 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(lines)