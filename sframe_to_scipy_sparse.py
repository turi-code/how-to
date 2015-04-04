import graphlab as gl

def sframe_to_scipy(x, column_name):
    assert x[column_name].dtype() == dict, \
        "The chosen column must be dict type, representing sparse data."
    # Create triples of (row_id, feature_id, count).
    # 1. Add a row number.
    x = x.add_row_number()
    # 2. Stack will transform x to have a row for each unique (row, key) pair.
    x = x.stack(column_name, ['feature', 'value'])

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

    # Map words into integers using a OneHotEncoder feature transformation.
    f = gl.feature_engineering.OneHotEncoder(features=['feature'])

    # We first fit the transformer using the above data.
    f.fit(x)

    # The transform method will add a new column that is the transformed version
    # of the 'word' column.
    x = f.transform(x)

    # Get the feature mapping.
    mapping = f['feature_encoding']

    # Get the actual word id.
    x['feature_id'] = x['encoded_features'].dict_keys().apply(lambda x: x[0])

    # x now has additional columns
    # +----+-------+------------------+---------+
    # | id | value | encoded_features | word_id |
    # +----+-------+------------------+---------+
    # | 0  |  5.0  |      {0: 1}      |    0    |
    # | 0  |  1.0  |      {1: 1}      |    1    |
    # | 1  |  10.0 |      {2: 1}      |    2    |
    # | 1  |  3.0  |      {1: 1}      |    1    |
    # +----+-------+------------------+---------+

    # Create numpy arrays that contain the data for the sparse matrix.
    import numpy as np
    i = np.array(x['id'])
    j = np.array(x['feature_id'])
    v = np.array(x['value'])
    width = x['id'].max() + 1
    height = x['feature_id'].max() + 1

    # Create a sparse matrix.
    from scipy.sparse import csr_matrix
    mat = csr_matrix((v, (i, j)), shape=(width, height))

    return mat, mapping

# Original data.
x = gl.SFrame({'features': [{'hello': 1.0, 'bob': 5},
                            {'hello': 3.0, 'john': 10}]})

m, f = sframe_to_scipy(x, 'features')

# The m object is now a sparse matrix representing x.
# >>> m
# <2x3 sparse matrix of type '<type 'numpy.float64'>'
#         with 4 stored elements in Compressed Sparse Row format>
# >>> m.todense()
# matrix([[  5.,   1.,   0.],
#         [  0.,   3.,  10.]])

# The f object provides an SFrame with the following format:
# >>> f
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

