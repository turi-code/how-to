import graphlab as gl
from graphlab_util.timezone import GMT
from datetime import datetime

d1 = datetime(2011, 1, 21, 7, 7, 21, tzinfo=GMT(0))
d2 = datetime(2010, 2, 5, 7, 8, 21, tzinfo=GMT(4.5))

sa = gl.SArray([d1,d2])
sa.split_datetime(column_name_prefix="",limit=['year','month'],tzone=True)
print sa
