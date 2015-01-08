#!/usr/bin/python

import os, sys, paramiko, signal, getpass, platform



class user(object):
    def __init__(self, username, password):
        self.name = username
        self.passwd = password
        self.hostlist = []
    
    def add_host(self, name):
        self.hostlist.append(name)
        
def execute(host, name, passwd, cmd):
    t = paramiko.Transport((host, 22))
    t.connect(username=name, password=passwd, hostkey=None)
    channel = t.open_channel(kind = "session")
    channel.exec_command(cmd)
    output = channel.makefile('rb', -1).readlines()
    for lines in output:
        lines = lines.strip()
        print lines


def main():
    sys.stdout.write("Username: ")  
    username = raw_input()
    password = getpass.getpass()
    u = user(str(username), str(password))
    
    os = platform.system()
    print os
    
    if os == "Darwin":
        file = '/Users/' + username + '/.ssh/known_hosts'
    else:
        file = '/home/' + username + '/.ssh/known_hosts'
        
    f = open(file, 'r')
    hosts = []
    for line in f:
        hosts.append(str(line.split()[0]))
    for h in hosts:
        if str(h).find("ca") != -1:
            h = h[:str(h).find("ca")+2]
            u.add_host(str(h))
    if len(hosts) == 0:
        print "Could not find (Canadian) hosts in known_hosts, you must manually input them."
        exit()
    
    top = "top -b -u " + u.name + " -n 1 | grep " + u.name
    qstat = "qstat -u " + u.name
    commands = [top, qstat]
    
    for host in u.hostlist:
        print "\n", host
        print "_____________________________"
        for cmd in commands:
            print "\n", cmd.split()[0]
            print "_____________________________"
            execute(host, u.name, u.passwd, cmd)

if __name__ == "__main__":
    main()

