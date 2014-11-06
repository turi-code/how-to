
# To perform basic math operations on each row of an SArray (or a column of an SFrame)
# it is most efficient to utilize the .apply method and specify a lambda function.
#
# For API documentation on the .apply() method, see here:
# http://graphlab.com/products/create/docs/generated/graphlab.SArray.apply.html#graphlab.SArray.apply

import math
import graphlab
import timeit

# create an SArray with 1,000,000 rows
sa = graphlab.SArray(range(1, 1000001))

# Log: We want to get the log for each of the rows in the SArray.
logs = sa.apply(lambda x: math.log(x))

# Getting the absolute value for each row:
pos = sa.apply(lambda x: abs(x))

# When performing other basic stats operations, it is much more efficient to 
# use the implementations provided by SArrays. This avoids implicit 
# conversions to Python lists and keeps the operations in the C++ engine.
# Examples:
mean = sa.mean()
max = sa.max()
min = sa.min()
std = sa.std()

sa_results = timeit.timeit(stmt='sa.max()', setup='import graphlab; sa = graphlab.SArray(range(1,1000001))', number=1)
max_results = timeit.timeit(stmt='max(sa)', setup='import graphlab; sa = graphlab.SArray(range(1,1000001))', number=1)

print "Using max(sa): %g" % max_results         # laptop results: 1.79631s
print "Using SArray.max(): %g" % sa_results     # laptop results: 0.015002s
