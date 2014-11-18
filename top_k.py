#Title: How to find the top-k values in a column for each value of a different
#grouping column.

# This technique is best for small values of k. For large values of k, it can be
# more efficient to use SFrame stack and a lambda function to sort.

import graphlab as gl

# Construct the data
county_population = [('CA', 'Orange', 3055745),
                     ('TX', 'Dallas', 2416014),
                     ('CA', 'Riverside', 5217080),
                     ('NY', 'Kings', 2532645),
                     ('CA', 'San Diego', 3140069),
                     ('CA', 'Los Angeles', 9889056),
                     ('TX', 'Bexar', 1756153),
                     ('NY', 'Suffolk', 1498816),
                     ('NY', 'Queens', 2247848),
                     ('TX', 'Harris', 4180894),
                     ('TX', 'Tarrant', 1849815),
                     ('NY', 'New York', 1601948)]

states, counties, populations = [list(x) for x in zip(*county_population)]
sf = gl.SFrame({'State': states, 'County': counties, 'Population': populations})

# SFrame sort and groupby to find the top 2 counties by population in each state
sf = sf.sort(['State', 'Population'], ascending=False)
sf = sf.add_row_number('id')
grp = sf.groupby('State', gl.aggregate.MIN('id'))
sf = sf.join(grp, 'State', how='left')
sf['rank'] = sf['id'] - sf['Min of id']
top_k = sf[sf['rank'] < 2]

# Returns:
# +----+-------------+------------+-------+-----------+------+
# | id |    County   | Population | State | Min of id | rank |
# +----+-------------+------------+-------+-----------+------+
# | 0  |    Harris   |  4180894   |   TX  |     0     |  0   |
# | 1  |    Dallas   |  2416014   |   TX  |     0     |  1   |
# | 4  |    Kings    |  2532645   |   NY  |     4     |  0   |
# | 5  |    Queens   |  2247848   |   NY  |     4     |  1   |
# | 8  | Los Angeles |  9889056   |   CA  |     8     |  0   |
# | 9  |  Riverside  |  5217080   |   CA  |     8     |  1   |
# +----+-------------+------------+-------+-----------+------+
