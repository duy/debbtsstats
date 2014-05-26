#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Helper functions to get a list of dates and total number bugs open by certain 
persons.
"""

__author__ = "duy <duy at rhizoma dot tk>"                                      
__copyright__ = "GPL v3"  

#FIXME: check possibility several bugs same day

from util import date_range_list


# add here new person to include in the stats.
# choose name string that are unique in bts originator
PERSONS = ['Levsen', 'Beckmann',  'Treinen', 'Steele', 'Nussbaum', 'Martens', 
    'arno@debian.org']


def initialize_bugs_by_person_dict(value,  otherperson=None):
    """ Returns a dictionary with persons as keys and number of bugs as values.
    
    >>> initialize_bugs_by_person_dict(0,'other')
    {'Beckmann': 0,
     'Levsen': 0,
     'Martens': 0,
     'Nussbaum': 0,
     'Steele': 0,
     'Treinen': 0,
     'arno@debian.org': 0,
     'other': 0}
    """
    personbugsdict = dict([(person,  value) for person in PERSONS])
    person
    if otherperson:
        personbugsdict[otherperson] = value
    return personbugsdict


def initialize_bugs_by_person_by_date_dict(datelist):
    """ Returns a dictionary where the keys are dates and the values are 
    dictionaries with persons as keys and number of bugs.
      
    >>> initialdate = datetime(2014,1,1).date()
    >>> datelist = date_range_list(initialdate)
    >>> initialize_bugs_by_person_by_date_dict(datelist)
     { datetime.date(2014, 5, 22): {'Beckmann': 0,
      'Levsen': 0,
      'Martens': 0,
      'Nussbaum': 0,
      'Steele': 0,
      'Treinen': 0,
      'arno@debian.org': 0}
      ...
    """

    return dict([(idate, initialize_bugs_by_person_dict(0, 'other'))
        for idate in datelist])


def date_person_dict(bugs):
    """ Return a dictionary where keys are date and values are persons 
    that open bugs that date.
    
    >>> bugs = load_bug_data(os.path.join(basepath,'data','btshistory.pickle')
    >>> date_person_list(bugs)
    {datetime.date(2014, 5, 15): u'Holger Levsen <holger@layer-acht.org>'}
    """

    return dict(sorted([(bug.date.date(), bug.originator) 
        for bug in bugs if bug.done]))


def get_person_by_originator(originator):
    """ Get the person in PERSONS list from the bug.originator field.
    """

    for person in PERSONS:
        if originator.find(person)>-1:
            return person
    return 'other'


#FIXME: refactor
#FIXME: such a long name!
def bugs_by_person_by_date_dict(bugs, initialdate, enddate=None):
    """ Returns a dictionary where keys are dates and values are dictionaries 
    with persons as key and total number of open bugs as values.
    
    
    >>> bugs = load_bugs(os.path.join(basepath,'data','btshistory.pickle')
    >>> initialdate = datetime(2014,1,1).date()
    >>> datelist = date_range_list(initialdate)
    >>> bugsbypersonbydatedict = initialize_bugs_by_person_by_date_dict(datelist)
    >>> datepersondict = date_person_dict(bugs)
    >>> newbugsbypersonbydatedict = bugs_by_person_by_date_dict(datepersondict, 
    bugsbypersonbydatedict, initialdate)
    
    """

    if not enddate:
        enddate = date.today()

    datelist = date_range_list(initialdate)
    bugsbypersonbydatedict = initialize_bugs_by_person_by_date_dict(datelist)
    datepersondict = date_person_dict(bugs)
    totalbugsbyperson = initialize_bugs_by_person_dict(0, 'other')
    lastdatebugbyperson = initialize_bugs_by_person_dict(initialdate, 'other')


    for idate in sorted(bugsbypersonbydatedict.keys()):
        originator = datepersondict.get(idate, None)
        # if there's a bug open this day by somebody
        if originator:
            person = get_person_by_originator(originator)
            if totalbugsbyperson[person] > 0:
                # fill up the previous dates with the last number of bugs
                daterange = date_range_list(lastdatebugbyperson[person],  idate)
                for d in daterange:
                    bugsbypersonbydatedict[d][person] = totalbugsbyperson[person] 
            # update the current date
            totalbugsbyperson[person] +=1
            bugsbypersonbydatedict[idate][person]= totalbugsbyperson[person]
            lastdatebugbyperson[person] = idate
    #fill  up last dates to endate
    for person, lastdate in lastdatebugbyperson.items():
        daterange = date_range_list(lastdate, enddate)
        for d in daterange:
            bugsbypersonbydatedict[d][person] = totalbugsbyperson[person] 
    return bugsbypersonbydatedict

def save_bugs_by_person_by_date(bugsbypersonbydatedict, filepath):
    """Save bugs_by_person_by_date_dict to csv file """

    # when adding a new person to the list of persons, update this list too
    bugsbydatebypersonlist = sorted(
        [(d.strftime('%Y%m%d'),values['Levsen'],
            values['Beckmann'],values['Treinen'],values['Steele'], 
            values['Nussbaum'], values['Martens'], values['arno@debian.org'], 
            values['other']) 
                for d, values in bugsbypersonbydatedict.items()])
    with open(filepath,'w') as f:
        f.write('date, Levsen, Beckmann, Treinen, Steele, Nussbaum, Martens, \
                arno@debian.org, other\n')
        f.write('\n'.join(','.join(map(str,i)) for i in bugsbydatebypersonlist))
    print "Saved opened bugs by person and date to file %s" % filepath

