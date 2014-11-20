# Title: Convert a column of datetime strings into UNIX timestamps

import graphlab as gl
from datetime import datetime
from graphlab_util.timezone import GMT

sa = gl.SArray(['20-Oct-2011 09:30:10 GMT-05','22-Nov-2014 09:40:30 GMT-04',\
        '20-Jan-2012 08:34:10 GMT+02'])

# Boost date time from string conversion guide:
# http://www.boost.org/doc/libs/1_48_0/doc/html/date_time/date_time_io.html

sa_datetime = sa.str_to_datetime("%d-%b-%Y %H:%M:%S %ZP")
# Look at SArray.datetime_to_str() for reverse functionality

print gl.SFrame(sa_datetime)

#+---------------------------+
#|             X1            |
#+---------------------------+
#| 2011-10-20 09:30:10-05:00 |
#| 2014-11-22 09:40:30-04:00 |
#| 2012-01-20 08:34:10+02:00 |
#+---------------------------+
#[3 rows x 1 columns]

sa_timestamps = sa_datetime.astype(int)
print sa_timestamps

# [1319121010, 1416663630, 1327041250]


