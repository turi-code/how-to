import graphlab as gl

sf = gl.SFrame({'business': [1,2,3,4], 
                'category.retail': [1, None, 1, None],
                'category.food': [1, 1, None, 1],
                'category.service': [None, 1, 1, None],
                'category.shop': [1, 1, None, 1]})

# Pack the SFrame columns into a list
# +----------+--------------------+
# | business |      category      |
# +----------+--------------------+
# |    1     |  [1, 1, None, 1]   |
# |    2     |  [1, None, 1, 1]   |
# |    3     | [None, 1, 1, None] |
# |    4     | [1, None, None, 1] |
# +----------+--------------------+
sf_packed_list = sf.pack_columns(column_prefix='category', 
                                 new_column_name='category')

# Pack the columns into a dict
# +----------+--------------------------------+
# | business |            category            |
# +----------+--------------------------------+
# |    1     | {'food': 1, 'shop': 1, 're ... |
# |    2     | {'food': 1, 'shop': 1, 'se ... |
# |    3     |  {'retail': 1, 'service': 1}   |
# |    4     |     {'food': 1, 'shop': 1}     |
# +----------+--------------------------------+
sf_packed_dict  = sf.pack_columns(column_prefix='category', dtype=dict, 
                                  new_column_name='category')

