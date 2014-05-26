#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Script that retrieves bug status from the Debian bts using bts tool."""

__author__ = "duy <duy at rhizoma dot tk>"                                      
__copyright__ = "GPL v3"

import debianbts as bts
import pickle
import argparse


import os.path
basepath = os.path.dirname(os.path.dirname(os.path.abspath((__file__))))
#FIXME: to import the functions without installing
import sys
sys.path.insert(0,os.path.join(basepath,'debbtsstats/'))

from util import fetch_bugs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--bugsfile',  help='',
                        default = os.path.join(basepath,'data',
                                    'btshistory.pickle'))

    parser.add_argument('-e','--email', 
                        help='',
                        default="debian-qa@lists.debian.org")
    parser.add_argument('-u','--usertag', 
                        help='',
                        default="piuparts")
    args = parser.parse_args()

    fetch_bugs(args.bugsfile, args.email, args.usertag)

if __name__ == "__main__":
    main()                       
