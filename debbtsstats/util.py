#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Common util functions for debbtsstats"""

__author__ = "duy <duy at rhizoma dot tk>"                                      
__copyright__ = "GPL v3"  

import pickle
from datetime import timedelta, datetime, date

import debianbts as bts

# FIXME: handle filepath exceptions
def fetch_bugs(filepath, email, usertag):
    """Fetch the bugs from bts and save them in a pickle to don't have to query 
    bts again

    Return:
        list of debianbts.Bugreport items
    """
    bugnrlist = bts.get_usertag(email, usertag)
    bugs = bts.get_status(bugnrlist[usertag])
    with open(filepath,'w') as f:
        pickle.dump(bugs,f)
    print 'saved bts history to %s ' % filepath
    return bugs


# FIXME: handle filepath exceptions
def load_bugs(filepath):   
    """Load the debianbts bugs from a pickle file.
    """
    with open(filepath) as f:
        bugs = pickle.load(f)
    print 'loaded bts history from %s' % filepath
    return bugs


def date_range_list(initialdate, enddate=None):
    """Return list of dates in a date range. 
    
    >>> initialdate = datetime(2005,1,1).date()
    >>> date_range_list(initialdate)
    [datetime.date(2005, 1, 1),
     datetime.date(2005, 1, 2),
     ...
    """
    
    if not enddate:
        enddate = date.today()
    datelist = [initialdate + timedelta(days=d) 
        for d in range(0, (enddate - initialdate).days)]
    return datelist

