# Import/Export data from Pandas
import graphlab as gl
import pandas as pd

# Pandas series can be converted to graphlab SArrays.
pd_series = pd.Series([1,2,3,4,5])
gl_sarray = gl.SArray(pd_series)
print gl_sarray
# [1, 2, 3, 4, 5]

# Pandas data frames can be converged to graphlab SFrames.
pd_dataframe = pd.DataFrame({
     'one' : pd.Series([1., 2., 3., 4.]),
     'two' : pd.Series([5., 6., 7., 8.])})
gl_sframe = gl.SFrame(pd_dataframe)
print gl_sframe
# +-----+-----+
# | one | two |
# +-----+-----+
# | 1.0 | 5.0 |
# | 2.0 | 6.0 |
# | 3.0 | 7.0 |
# | 4.0 | 8.0 |
# +-----+-----+
# [4 rows x 2 columns]

# You can also convert the SFrame to pandas dataframes. 
# Note that Pandas is limited by the size of the memory.
pd_dataframe = gl_sframe.to_dataframe()
print pd_dataframe
#    one  two
#    0    1    5
#    1    2    6
#    2    3    7
#    3    4    8
