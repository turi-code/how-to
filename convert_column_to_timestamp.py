# Title: Convert a column of datetime strings into UNIX timestamps
import graphlab as gl

# Define a SFrame. Here the date-time is of type str
sf = gl.SFrame({'datetime-as-string': ['20-Oct-2011 09:30:10 GMT-05',
                             '22-Nov-2014 09:40:30 GMT-04', 
                             '20-Jan-2012 08:34:10 GMT+02']})

# Boost date time from string conversion guide:
# http://www.boost.org/doc/libs/1_48_0/doc/html/date_time/date_time_io.html
# Look at datetime_to_str() function (for SArrays) for reverse functionality
sf['datetime'] = sf['datetime-as-string'].str_to_datetime("%d-%b-%Y %H:%M:%S %ZP")
print sf
# +-----------------------------+---------------------------+
# |      datetime-as-string     |          datetime         |
# +-----------------------------+---------------------------+
# | 20-Oct-2011 09:30:10 GMT-05 | 2011-10-20 09:30:10-05:00 |
# | 22-Nov-2014 09:40:30 GMT-04 | 2014-11-22 09:40:30-04:00 |
# | 20-Jan-2012 08:34:10 GMT+02 | 2012-01-20 08:34:10+02:00 |
# +-----------------------------+---------------------------+

# Convert to UNIX time stamps
unix_time_stamps = sf['datetime'].astype(int)
print unix_time_stamps
# [1319121010, 1416663630, 1327041250]


