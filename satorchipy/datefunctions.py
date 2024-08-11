"""
$Id: datefunctions.py
$auth: Steve Torchinsky <steve@satorchi.net>
$created: Mon 26 Aug 2013 12:26:05 CEST

some useful date functions 
take from tools_embraceStats and from ObsFunctions

$modified: Thu 05 Sep 2013 12:12:21 CEST
  adding more possibilities to str2dt : assuming a time on the given day

$modified: Mon 07 Jul 2014 17:05:32 CEST
  str2dt() : correctly deal with FITS comment on multiple lines

$modified: Wed 25 Feb 2015 11:48:52 CET
  str2dt() : added format for isodate used in filenames for pulsar data

$modified: Tue  7 Apr 15:37:43 CEST 2015
  roundTime() : round time to nearest minute (or whatever) 

$modified: Wed 10 Jun 2015 13:57:17 CEST
  str2dt() : read posixly correct date format

$modified: Thu 16 Jul 2015 15:07:19 CEST
  str2dt() : read date in format: Jul 16 15:10:52  2015 for LCU pinglog

$modified: Fri 14 Aug 2015 15:28:50 CEST
  str2dt() : read date in stupid day.month.year format

$modified: Fri 29 Jul 2016 15:25:25 CEST
  str2dt() : now = NOW

$modified: Thu 06 Jul 2017 07:43:37 CEST
  str2dt() : read date in format YYYYMMDDTHHMMSS

$modified: Tue 26 Sep 2017 10:19:54 CEST
  moved to satorchipy: My python gadgets on github

"""
import datetime as dt
import re
import numpy as np

def isodate(date):
    return date.strftime('%Y-%m-%d %H:%M:%S.%f UT')

def str2dt(datestr):
    if isinstance(datestr,dt.datetime): return datestr

    if not isinstance(datestr,str):
        print('date conversion:  argument must be a string')
        return None

    dtnow=dt.datetime.utcnow()
    if datestr=="tomorrow":
        return dt.datetime(dtnow.year,dtnow.month,dtnow.day)+dt.timedelta(days=1)

    if datestr.upper()=="NOW": return dtnow

    datestr=datestr.strip()
    datestr=datestr.replace("CONTINUE","").replace("'","") # fits file comment continued on next line
    datestr=re.sub(' UT.*','',datestr) # remove time zone identifier

    # dates sent from a French Windows machine
    datestr=re.sub('[dD].c\.','12',datestr)
    datestr=re.sub('[nN]ov\.','11',datestr)
    datestr=re.sub('[oO]ct\.','10',datestr)
    datestr=re.sub('[sS]ep\.','9',datestr)
    datestr=re.sub('[sS]ept\.','9',datestr)
    datestr=re.sub('[aA]o.t\.','8',datestr)
    datestr=re.sub('[aA]o.t','8',datestr)
    datestr=re.sub('[aA]o.\.','8',datestr)
    datestr=re.sub('[jJ]ui\.','7',datestr)
    datestr=re.sub('[jJ]uil\.','7',datestr)
    datestr=re.sub('[jJ]uil','7',datestr)
    datestr=re.sub('[jJ]un\.','6',datestr)
    datestr=re.sub('[mM]ai','5',datestr)
    datestr=re.sub('[aA]vr\.','4',datestr)
    datestr=re.sub('[jJ]an\.','1',datestr)
    datestr=re.sub('[jJ]anv\.','1',datestr)
    datestr=re.sub('[fF].vr\.','2',datestr)
    datestr=re.sub('[fF].v\.','2',datestr)
    datestr=re.sub('[mM]ar\.','3',datestr)
    datestr=re.sub('[mM]ars','3',datestr)
    datestr=datestr.replace(',','.')
    
    fmts=["%Y-%m-%d %H:%M:%S.%f",
          "%Y-%m-%d %H:%M:%S",
          "%Y-%m-%d %H:%M:%SZ",
          "%Y-%m-%d %H:%M:%S.%fZ",
          '%Y-%m-%d %H:%M:%S.%f UT',
          '%Y-%m-%d %H:%M:%S UT',
          "%Y-%m-%d %H:%M",
          "%Y-%m-%dT%H:%M:%S.%f",
          "%Y-%m-%dT%H:%M:%S",
          "%Y-%m-%dT%H:%M:%SZ",
          "%Y-%m-%dT%H:%M:%S.%fZ",
          '%Y-%m-%dT%H:%M:%S.%f UT',
          '%Y-%m-%dT%H:%M:%S UT',
          "%Y-%m-%dT%H:%M",          
          "%Y-%m-%d",
          "%Y-%b-%d %H:%M:%S.%f",
          "%Y-%b-%d %H:%M:%S",
          "%Y-%b-%d %H:%M:%SZ",
          "%Y-%b-%d %H:%M:%S.%fZ",
          '%Y-%b-%d %H:%M:%S.%f UT',
          '%Y-%b-%d %H:%M:%S UT',
          "%Y-%b-%d %H:%M",
          "%Y-%b-%dT%H:%M:%S.%f",
          "%Y-%b-%dT%H:%M:%S",
          "%Y-%b-%dT%H:%M:%SZ",
          "%Y-%b-%dT%H:%M:%S.%fZ",
          '%Y-%b-%dT%H:%M:%S.%f UT',
          '%Y-%b-%dT%H:%M:%S UT',
          "%Y-%b-%dT%H:%M",          
          "%Y-%b-%d",
          "%Y%m%d",
          "%Y%m%d-%H%M",
          "D%Y%m%dT%H%M%S",
          "%a %b %d %H:%M:%S %Y",
          "%b %d %H:%M:%S  %Y",
          "%d.%m.%Y  %H:%M",
          "%Y%m%dT%H%M%S",
          "%Y%m%dT%H%M%S.%f",
          "%Y%m%d-%H%M%S.%f",
          "%Y%m%d-%H%M%S",
          "%Y-%m-%d_%H.%M.%S",
          "%Y%m%dT%H%M%SZ"]


    for fmt in fmts:
        try: return dt.datetime.strptime(datestr,fmt)
        except: pass

    # special cases, assuming some time today
    ymd=dtnow.strftime('%Y-%m-%d')
    datestr_today=ymd+' '+datestr
    for fmt in fmts:
        try: return dt.datetime.strptime(datestr_today,fmt)
        except: pass    

    # another special case:  fractional seconds given with only 3 places
    datestr_today=datestr+'000'
    for fmt in fmts:
        try: return dt.datetime.strptime(datestr_today,fmt)
        except: pass        

    print("did not convert date string to datetime.  returning None: >>%s<<" % datestr_today)
    return None

# convert a timedelta to total number of seconds
def tot_seconds(delta):
    tsecs=delta.days*24*3600 + delta.seconds + delta.microseconds*1e-6
    return tsecs

# round time to nearest minute (or whatever)
# taken from stackoverflow
# http://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object-python/10854034#10854034
def roundTime(d=None, roundTo=60):
   """Round a datetime object to any time laps in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if d == None : d = dt.datetime.utcnow()
   seconds = (d - d.min).seconds
   # // is a floor division, not a comment on following line:
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return d + dt.timedelta(0,rounding-seconds,-d.microsecond)

def tstamp2dt(tstamp):
    '''
    convert a timestamp to a datetime object
    '''
    if not (isinstance(tstamp,list) or isinstance(tstamp,np.ndarray)):
        return dt.datetime.utcfromtimestamp(tstamp)

    date = []
    for val in tstamp:
        date.append(dt.datetime.utcfromtimestamp(val))
    date = np.array(date)
    return date
