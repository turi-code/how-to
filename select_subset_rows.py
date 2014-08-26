# Title: How to filter/select rows from an SFrame.
import graphlab as gl
from datetime import datetime

# An SFrame with sample Flight data.
sf = gl.SFrame({
'id'         : [1,2,3],
'flight_time': [120,12,-2],
'carrier'    : ['BA','LY','US'],'plane_type':[727,737,777]})

# Select only rows with positive flight_time.
# ----------------------------------------------------------------------------
# Note: Method 1 will be faster than Method 2, but Method 2 is more flexible.

# Method 1: SFrame Logical Filter
sf_filter = sf[sf['flight_time'] > 0] 
# Method 2: SFrame apply() function
sf_filter = sf[sf.apply(lambda x: x['flight_time'] > 0)] 

# Select flights from either carriers 'US' or 'LY' or plane type 727
# ----------------------------------------------------------------------------
# Using Method 1
sf_filter = sf[(sf['carrier'] == 'US') | (sf['carrier'] == 'LY') | (sf['plane_type'] == 727)]
# Using Method 2
sf_filter = sf[sf.apply(lambda x: True if (x['carrier'] == 'US' or x['carrier'] == 'LY' or x['plane_type'] == 727) else False)]

