'''
$Id: __init__.py<satorchipy>
$auth: Steve Torchinsky <satorchi@apc.in2p3.fr>
$created: Tue 26 Sep 2017 11:11:17 CEST
$license: GPLv3 or later, see https://www.gnu.org/licenses/gpl-3.0.txt

          This is free software: you are free to change and
          redistribute it.  There is NO WARRANTY, to the extent
          permitted by law.

satorchipy is a package of my python gadgets

'''
from .datefunctions import\
    isodate,\
    str2dt,\
    tot_seconds,\
    roundTime

from .quickplot import\
    quickplot
