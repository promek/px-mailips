#!/usr/bin/env python
# -*- coding: utf8 -*-

#######################################################################
# px-mailips
# cpanel sunucularda /etc/mailips dosyasina resellerlara göre ip atamasi yapar...
#
# Copyright (C) 2012 by ibrahim ŞEN <ibrahim@promek.net>
#
# https://github.com/promek/px-mailips
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>
#######################################################################

import os
import sys

CPUSERS_PATH = "/var/cpanel/users" #/var/cpanel/users
MAILIPS_FILE = "/etc/mailips" #/etc/mailips
PXCONF_FILE = "/etc/px-mailips.conf" #/etc/px-mailips.conf

def getOwnerDomain(file) :
    DNS=""
    OWNER=""
    for line in open(file):
        line = line.strip().split("=")
        if (line[0] == 'DNS'):
            DNS=line[1]
        if (line[0] == 'OWNER'):
            OWNER=line[1]
    return OWNER,DNS


def main() :
    try :
        resellerip={}
        domainip=[]
        print "%s reloading..." % MAILIPS_FILE    
        for line in open(PXCONF_FILE):    
            line = line.strip().split(":")
            resellerip[line[0].strip()]=line[1].strip()
    
        for usrfile in os.listdir(CPUSERS_PATH):
            mips=getOwnerDomain(CPUSERS_PATH+"/"+usrfile)
            
            if mips[0] in resellerip.keys():
                domainip.append("%s: %s" % (mips[1],resellerip[mips[0]]))
            
        if "*" in resellerip.keys():
            domainip.append("%s: %s" % ('*',resellerip['*']))            
    
        mailipsfile = open(MAILIPS_FILE, "wb") 
    
        for item in domainip:
            mailipsfile.write("%s\n" % item)
        
        mailipsfile.close()
        print "done..."

    except Exception,e:
        print "failed...",e


def usage():
    print "Usage: px-mailips.py [OPTION]"
    print "-r : reload"
    print "-p : print"

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "-r":
            main()  
        elif sys.argv[1] == "-p":        
            cnfile = open(PXCONF_FILE)
            print "-> %s " % PXCONF_FILE 
            print cnfile.read()
            cnfile.close()
        else :
            usage()
    else:
        usage()
