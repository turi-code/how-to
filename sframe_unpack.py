import graphlab as gl

# An SFrame with a column 'wc' of type (dict) 
sf = gl.SFrame({'id': [1,2,3],
               'dict_col': [{'a': 1}, {'b': 2}, {'a': 1, 'b': 2}]})

sf_unpack = sf.unpack('dict_col', column_name_prefix="foo")
# Returns
#  +----+-------+-------+
#  | id | foo.a | foo.b |
#  +----+-------+-------+
#  | 1  |  1    | None  |
#  | 2  | None  |  2    |
#  | 3  |  1    |  2    |
#  +----+-------+-------+
