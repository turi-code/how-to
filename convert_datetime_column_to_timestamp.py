import graphlab as gl
from datetime import datetime

d1 = datetime(2014, 10, 13, 3, 31, 50)
d2 = datetime(2013, 11, 12, 4, 15, 56)
sa = gl.SArray([d1,d2])

sa_timestamps = sa.astype(int)
print sa_timestamps
