# Title: Parse a datetime column into its components (year, month, etc.)
import graphlab as gl
from graphlab_util.timezone import GMT
from datetime import datetime

# Define the inputs
d1 = datetime(2011, 1, 21, 7, 7, 21, tzinfo=GMT(0))
d2 = datetime(2010, 2, 5, 7, 8, 21, tzinfo=GMT(4.5))

# The SArray can store native datetime objects.
sa = gl.SArray([d1,d2])

result = sa.split_datetime(column_name_prefix="",limit=['year','month'],tzone=True)
print result
#+------+-------+-------+
#| year | month | tzone |
#+------+-------+-------+
#| 2011 |   1   |  0.0  |
#| 2010 |   2   |  4.5  |
#+------+-------+-------+
#[2 rows x 3 columns]

result = sa.split_datetime(column_name_prefix="res",limit=['day','hour','minute','second'])
print result
#+---------+----------+------------+------------+
#| res.day | res.hour | res.minute | res.second |
#+---------+----------+------------+------------+
#|    21   |    7     |     7      |     21     |
#|    5    |    7     |     8      |     21     |
#+---------+----------+------------+------------+
#[2 rows x 4 columns]
