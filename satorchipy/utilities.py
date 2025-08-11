'''
$Id: utilities.py<satorchipy>
$auth: Steve Torchinsky <satorchi@apc.in2p3.fr>
$created: Mon 11 Aug 2025 10:10:28 CEST
$license: GPLv3 or later, see https://www.gnu.org/licenses/gpl-3.0.txt

          This is free software: you are free to change and
          redistribute it.  There is NO WARRANTY, to the extent
          permitted by law.

some utilities I use
'''
import sys,os,re
from satorchipy.datefunctions import str2dt

def assign_value(val_str):
    '''
    assign a value from a string

    if unsuccessful, return the string
    '''

    # first check if it is a date
    val = str2dt(val_str)
    if val is not None: return val

    # check if it is a number
    try:
        val = eval(val_str)
    except:
        return val_str
    return val

def parseargs(argv,expected_args=None):
    '''
    parse command line arguments and assign values

    argv is the list of command line arguments, as per sys.argv
    
    expected_args is a list of possible options that might appear on the command line
    If not found, they are given the value of None in the return dictionary
    '''

    options = {}
    if expected_args is not None:
        for arg in expected_args:
            options[arg] = None
    
    for arg in argv:
        # remove leading dashes        
        if arg.find('--')==0:
            arg = arg[2:]
        
        match  = re.search('(.*)=',arg)
        if match:
            arg_str = match.groups()[0]
            
            val_str = arg.split('=')[-1]
            val = assign_value(val_str)
            options[arg_str] = val
            continue

        # if the argument is on its own, assume it is a boolean option
        option[arg] = True
        continue

    return options
