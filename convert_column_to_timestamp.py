# Title: Convert a date string column to a UNIX timestamp
import graphlab as gl
from datetime import datetime
# Requires you to 'pip install python-dateutil==1.5'
from dateutil import parser

def str_to_timestamp(the_str):
    try:
        dt = parser.parse(the_str)
    except:
        return None

    # UNIX epoch is January 1, 1970
    return (dt - datetime(1970,1,1)).total_seconds()

# 02/29/2001 is invalid, so should be 'None' in output
sf = gl.SFrame({'date':['2000-08-21','2013-06-08 17:25:00.12753','02/29/2001'],'id':[1,2,3]})
sf['date'] = sf['date'].apply(str_to_timestamp)
