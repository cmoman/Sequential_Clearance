#!/usr/bin/env python
import subprocess

def uname_func():
    uname = 'uname'
    uname_arg = '-a'
    print "Gathering system information with %s comand:\n" % uname
    subprocess.call([uname, uname_arg])

def disk_func():
    diskspace ='df'
    diskspace_arg ='-h'
    print "Gathering disk space information %s command:\n" % diskspace
    subprocess.call([diskspace, diskspace_arg])

def main():
    uname_func()
    disk_func()

if __name__== "__main__":
    main()