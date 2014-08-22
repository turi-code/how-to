# Title: How to filter/select rows from an SFrame.
import graphlab as gl
from datetime import datetime

# An SFrame with sample Flight data.
sf = gl.SFrame({
'id'         : [1,2,3],
'flight_time': [120,12,-2],
'carrier'    : ['BA','LY','US'],'plane_type':[727,737,777]})
print sf

# Method 1: SFrame Logical Filter
# Select only rows with positive flight_time.
sf_filter = sf[sf['flight_time'] > 0] 

# Method 2: SFrame apply() function
# Select flights from either carriers 'US' or 'LY' or plane type 727
sf_filter = sf[sf.apply(lambda x: True if (x['carrier'] == 'US' or x['carrier'] == 'LY' or x['plane_type'] == 727) else False)]

