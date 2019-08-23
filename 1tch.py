import sys
import os
import subprocess
import csv
import glob
import threading 

import inifile # pip install inifile

ignore_commit_hashes = [ 'a202836f' ]

lines = [ ['name', 'desc', 'filesize', 'created', 'last_modified'] ]

def get_git_log(pathedname):
    log_lines = subprocess.Popen(f'git log --follow --format="%h,%at" {pathedname}', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    log_lines = log_lines.split('\n')
    del log_lines[-1] # last entry empty
    return log_lines

def git_log_head_to(filename, git_format='%h,%at'):
    log_lines = subprocess.Popen(f'git log --format="{git_format}" -1 > {filename}', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip()
    
def get_last_modified_commit(log_lines):
        i = 0
        for ignore_hash in ignore_commit_hashes: 
            if ignore_hash in log_lines[i]:
                i += 1
        return log_lines[i]

def get_created_commit(log_lines):
        i = len(log_lines) - 1
        for ignore_hash in ignore_commit_hashes: 
            if ignore_hash in log_lines[i]:
                i -= 1
        return log_lines[i]

def get_line(filename, pathedname):
    ini = inifile.IniFile(pathedname)

    name = filename    
    desc = ini.get('vars.desc', '<NULL>')
    filesize = ini.get('vars.filesize', '<NULL>')
    log_lines = get_git_log(pathedname)
    created = get_created_commit(log_lines).split(',')[1]
    last_modified = get_last_modified_commit(log_lines).split(',')[1]
    
    return [ name, desc, filesize, created, last_modified]

def set_lines(directory, wildcardname):
    pathname = os.path.join(directory, wildcardname)
    for fullname in glob.glob(pathname):
        path, filename = os.path.split(fullname)
        line = get_line(filename, fullname)
        lines.append(line)
        #print(line)
        #print('.', end = '')

def main(directory):
    cwd = os.getcwd()

    os.chdir(directory) # for git to function correctly
    
    thread_args = [ (directory, '[0-9]*',), 
                    (directory, '[a-d]*',), 
                    (directory, '[e-h]*',), 
                    (directory, '[i-l]*',), 
                    (directory, '[m-p]*',), 
                    (directory, '[q-t]*',), 
                    (directory, '[u-z]*',), 
                ]  

    threads = []
    for t_arg in thread_args:
        t = threading.Thread(target=set_lines, args=t_arg)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join() # wait for all threads

    os.chdir(cwd) # save csv to old cwd
    with open('pages/pkgs.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(lines)
    git_log_head_to('pages/extracted.csv', '%h,%aD')

if __name__ == '__main__':
    main(sys.argv[1])