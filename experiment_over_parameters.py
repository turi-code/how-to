# The following two utility functions are useful when you want
# to try out a variety of argument values for a given function.

import graphlab as gl
import itertools

def crossproduct(d):
    """
    Create an SFrame containing the crossproduct of all provided options.

    Parameters
    ----------
    d : dict
        Each key is the name of an option, and each value is a list
        of the possible values for that option.

    Returns
    -------
    out : SFrame
        There will be a column for each key in the provided dictionary,
        and a row for each unique combination of all values.

    Example
    -------
    settings = {'argument_1':[0, 1],
                'argument_2':['a', 'b', 'c']}
    print crossproduct(settings)
    +------------+------------+
    | argument_2 | argument_1 |
    +------------+------------+
    |     a      |     0      |
    |     a      |     1      |
    |     b      |     0      |
    |     b      |     1      |
    |     c      |     0      |
    |     c      |     1      |
    +------------+------------+
    [6 rows x 2 columns]
    """
    d = [zip(d.keys(), x)
                for x in itertools.product(*d.values())]
    sa = [{k:v for (k,v) in x} for x in d]
    return gl.SArray(sa).unpack(column_name_prefix='')

def map_across_rows(my_function, argument_sf):
    """
    Run a function using the arguments provided by each row in the SFrame.
    The function is assumed to return a dict.

    Example
    -------
    def f(argument_1, argument_2):
        return {'my_metric': argument_1 * argument_2}

    settings = {'argument_1':[0, 1],
                'argument_2':[0, 5, 10]}
    sf = crossproduct(settings)
    sf['results'] = map_across_rows(f, sf)

    Columns:
      argument_2  int
      argument_1  int
      results dict

    Rows: 6

    Data:
    +------------+------------+-------------------+
    | argument_2 | argument_1 |      results      |
    +------------+------------+-------------------+
    |     0      |     0      |  {'my_metric': 0} |
    |     0      |     1      |  {'my_metric': 0} |
    |     5      |     0      |  {'my_metric': 0} |
    |     5      |     1      |  {'my_metric': 5} |
    |     10     |     0      |  {'my_metric': 0} |
    |     10     |     1      | {'my_metric': 10} |
    +------------+------------+-------------------+
    [6 rows x 3 columns]
    """
    my_settings = argument_sf.pack_columns(dtype=dict)['X1']
    res = [my_function(**args) for args in my_settings]
    return gl.SArray(res)


# Examples
def f(argument_1, argument_2):
    return {'my_metric': argument_1 * argument_2}

settings = {'argument_1':[0, 1],
            'argument_2':[0, 5, 10]}
sf = crossproduct(settings)
print sf

sf['results'] = map_across_rows(f, sf)
print sf


