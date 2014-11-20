# Title: Split a datetime column into year, month, and timezone

import graphlab as gl
from graphlab_util.timezone import GMT
from datetime import datetime

d1 = datetime(2011, 1, 21, 7, 7, 21, tzinfo=GMT(0))
d2 = datetime(2010, 2, 5, 7, 8, 21, tzinfo=GMT(4.5))

sa = gl.SArray([d1,d2])
res = sa.split_datetime(column_name_prefix="",limit=['year','month'],tzone=True)
print res

#+------+-------+-------+
#| year | month | tzone |
#+------+-------+-------+
#| 2011 |   1   |  0.0  |
#| 2010 |   2   |  4.5  |
#+------+-------+-------+
#[2 rows x 3 columns]

res = sa.split_datetime(column_name_prefix="res",limit=['day','hour','minute','second'])
print res

#+---------+----------+------------+------------+
#| res.day | res.hour | res.minute | res.second |
#+---------+----------+------------+------------+
#|    21   |    7     |     7      |     21     |
#|    5    |    7     |     8      |     21     |
#+---------+----------+------------+------------+
#[2 rows x 4 columns]
