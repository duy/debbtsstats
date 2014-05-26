#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Helper functions to get a list of dates and total number bugs open, close.
"""

__author__ = "duy <duy at rhizoma dot tk>"                                      
__copyright__ = "GPL v3"

from datetime import datetime, date, timedelta
import argparse

from util import fetch_bugs, load_bugs, date_range_list

RC_SEVERITY = [
    'serious',
    'grave',
    'critical'
]


def initialize_date_bug_dict(datelist):
    datebugdict = dict()
    for date in datelist: 
        datebugdict[date] = {'done_rc': 0, 'open_rc':0, 'done_other':0,'open_other':0}
    return datebugdict


def create_bug_date_dict(bugs, initialdate, enddate):
    datelist = date_range_list(initialdate,enddate)
    datebugdict = initialize_date_bug_dict(datelist)


    print "len bugs:", len(bugs)
    for bug in bugs:
            # if created before initialdate, count only from initial date
        if bug.date.date() < initialdate:
            print "created date minor than initialdate, so take last one"
            startdate = initialdate
        else:
            startdate = bug.date.date()
        if bug.done: 
            print "bug is done"
            # if done before initialdate, don't count it
            if bug.log_modified.date() < initialdate:
                print "bug was done before initialdate, ignore it"
                break
            daterangeopen = date_range_list(startdate,bug.log_modified.date())[:-1]
            daterangedone = date_range_list(bug.log_modified.date(),enddate)
            if bug.severity in RC_SEVERITY:
               print "bug is rc"     
               # fill up previous dates with open     
               for d in daterangeopen:
                   datebugdict[d]['open_rc'] += 1
               # fill up next dates with close  
               for d in daterangedone:
                   datebugdict[d]['done_rc'] += 1
            else:
               print "bug is not rc"
               # fill up previous dates with open     
               for d in daterangeopen:
                   datebugdict[d]['open_other'] += 1
               # fill up next dates with close  
               for d in daterangedone:
                   datebugdict[d]['done_other'] += 1
        else:
            print "bug is open"
            daterange = date_range_list(startdate, enddate)
            if bug.severity in RC_SEVERITY:
               print "bug is rc"
               for d in daterange:
                   datebugdict[d]['open_rc'] += 1
            else:
               print "bug is not rc"
               for d in daterange:
                   datebugdict[d]['open_other'] += 1
    return datebugdict


def save_bug_date_dict(datebugdict, filepath):
    # convert date dict to list of tubples (date, done_rc, open_rc, done_other, open_other)
    datebuglist = sorted([(d.strftime('%Y%m%d'),values['done_rc'],values['open_rc'],values['done_other'],values['open_other']) for d, values in datebugdict.items()])
    with open(filepath,'w') as f:
        f.write('date, done_rc, open_rc, done_other, open_other\n')
        f.write('\n'.join(', '.join(map(str,i)) for i in datebuglist))
    print "Saved bugs by date to file %s" % filepath


