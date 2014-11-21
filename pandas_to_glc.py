# Import/Export data from Pandas
import graphlab as gl
import pandas as pd

# Pandas series can be converted to graphlab SArrays.
pd_series = pd.Series([1,2,3,4,5], index=['a', 'b', 'c', 'd', 'e'])
gl_sarray = gl.SArray(pd_series)
print gl_sarray
# [1, 2, 3, 4, 5]

# Pandas data frames can be converged to graphlab SFrames.
pd_dataframe = pd.DataFrame({
     'one' : pd.Series([1., 2., 3.], index=['a', 'b', 'c']),
     'two' : pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])})
gl_sframe = gl.SFrame(pd_dataframe)
print gl_sframe
# [4 rows x 2 columns]
# +-----+-----+
# | one | two |
# +-----+-----+
# | 1.0 | 1.0 |
# | 2.0 | 2.0 |
# | 3.0 | 3.0 |
# | nan | 4.0 |
# +-----+-----+

# You can also convert the SFrame to pandas dataframes. 
# Note that Pandas is limited by the size of the memory.
pd_dataframe = gl_sframe.to_dataframe()
print pd_dataframe
#   one  two
#   0    1    1
#   1    2    2
#   2    3    3
#   3  NaN    4
