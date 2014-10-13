import graphlab as gl
from datetime import datetime
from graphlab_util.timezone import GMT

dt = datetime(2011, 10, 20, 14, 30, 10)
dt = dt.replace(tzinfo=GMT(0))
dt = dt.astimezone(GMT(-5))
sa = graphlab.SArray([dt])

# Boost date time from string conversion guide:
# http://www.boost.org/doc/libs/1_48_0/doc/html/date_time/date_time_io.html

sa_str = sa.datetime_to_str("%d-%b-%Y %H:%M:%S %ZP")
print sa_str
sa_datetime_back = sa_str.str_to_datetime("%d-%b-%Y %H:%M:%S %ZP")
print sa_datetime_back

