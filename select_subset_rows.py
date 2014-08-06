# Title: How to filter rows (select only a subset of a table rows), based on some rules defined by the user

import graphlab as gl
from datetime import datetime

# some fake flight data below
sf = gl.SFrame({'id':[1,2,3],'flight_time':[120,12,-2],'carrier':['BA','LY','US'],'plane_type':[727,737,777]})
print sf

# select only rows with positive flight_time:
sf1 = sf[sf.apply(lambda x: True if x['flight_time'] > 0 else False)]
print sf1

# select only flights from either carriers 'US' or 'LY' or plane type 727
sf2 = sf[sf.apply(lambda x: True if (x['carrier'] == 'US' or x['carrier'] == 'LY' or x['plane_type'] == 727) else False)]
print sf2

