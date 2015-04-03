import graphlab as gl

# Original data
x = gl.SFrame({'words': [{'hello': 1.0, 'bob': 5}, {'hello': 3.0, 'john': 10}]})

# Create triples of (row_id, word_id, count)
x = x.add_row_number()
x = x.stack('words', ['word', 'value'])

# x now looks like the following:
# Columns:
#         id      int
#         word    str
#         value   float
#
# Rows: 4
#
# Data:
# +----+-------+-------+
# | id |  word | value |
# +----+-------+-------+
# | 0  |  bob  |  5.0  |
# | 0  | hello |  1.0  |
# | 1  |  john |  10.0 |
# | 1  | hello |  3.0  |
# +----+-------+-------+
# [4 rows x 3 columns]

# Map words into integers using a OneHotEncoder feature transformation
f = gl.feature_engineering.OneHotEncoder(features=['word'])
f.fit(x)
x = f.transform(x)

# Get the actual word id.
x['word_id'] = x['encoded_features'].dict_keys().apply(lambda x: x[0])

# x now has additional columns
# +----+-------+------------------+---------+
# | id | value | encoded_features | word_id |
# +----+-------+------------------+---------+
# | 0  |  5.0  |      {0: 1}      |    0    |
# | 0  |  1.0  |      {1: 1}      |    1    |
# | 1  |  10.0 |      {2: 1}      |    2    |
# | 1  |  3.0  |      {1: 1}      |    1    |
# +----+-------+------------------+---------+

# Create numpy arrays
import numpy as np
i = np.array(x['id'])
j = np.array(x['word_id'])
v = np.array(x['value'])
width = x['id'].max() + 1
height = x['word_id'].max() + 1

# Create a sparse matrix
from scipy.sparse import csr_matrix
m = csr_matrix((v, (i, j)), shape=(width, height))
# >>> m
# <2x3 sparse matrix of type '<type 'numpy.float64'>'
#         with 4 stored elements in Compressed Sparse Row format>
# >>> m.todense()
# matrix([[  5.,   1.,   0.],
#         [  0.,   3.,  10.]])

# Get feature mapping
f['feature_encoding']

# This provides an SFrame with the following format:
# Columns:
#         feature str
#         category        str
#         index   int
#
# Rows: 3
#
# Data:
# +---------+----------+-------+
# | feature | category | index |
# +---------+----------+-------+
# |   word  |   bob    |   0   |
# |   word  |  hello   |   1   |
# |   word  |   john   |   2   |
# +---------+----------+-------+

