#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Script that retrieves bug status from the Debian bts using bts tool
and returns a list of dates and total number bugs open by certain persons
"""

__author__ = "duy <duy at rhizoma dot tk>"                                      
__copyright__ = "GPL v3"  

from datetime import datetime, date
import argparse

import os.path
basepath = os.path.dirname(os.path.dirname(os.path.abspath((__file__))))
#FIXME: to import the functions without installing
import sys
sys.path.insert(0,os.path.join(basepath,'debbtsstats/'))

from util import load_bugs, fetch_bugs
from bugsbypersonbydate import bugs_by_person_by_date_dict, \
    save_bugs_by_person_by_date


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
    parser.add_argument('-d','--initialdate',
                        help='initial date in the form yyyymmdd',
                        default = '20051001')
    parser.add_argument('-o','--outputfile',
                        help='',
                        default = os.path.join(basepath,'data',
                                    'bugsbypersonbydate.csv'))
    args = parser.parse_args()

    enddate = date.today()
    initialdate = datetime.strptime(args.initialdate,'%Y%m%d').date()
    #FIXME: check that the file exists or call fetch_bugs
    bugs = load_bugs(args.bugsfile)
    bugsbypersonbydatedict = bugs_by_person_by_date_dict(bugs, initialdate, enddate)
    save_bugs_by_person_by_date(bugsbypersonbydatedict, args.outputfile)

if __name__ == "__main__":
    main()
