# This technique works best of the proposed subgraph is small. It does not scale
# well if both graphs are large.

import graphlab as gl

def is_subgraph(subgraph, g, vert_id='__id', src_id='__src_id',
                dst_id='__dst_id'):
    """
    Check if `sub_g` is a subgraph of `g`. `vert_id`, `src_id`, and
    `dst_id` are the column names for vertex, source, and destination vertex
    IDs.
    """

    subgraph_flag = True

    ## Check if vertices are a subset
    sf_filter = g.vertices.filter_by(subgraph.vertices[vert_id], vert_id)
    if sf_filter.num_rows() < subgraph.vertices.num_rows():
        subgraph_flag = False

    ## Check if edges are a subset
    sf_join = subgraph.edges.join(g.edges, on=[src_id, dst_id], how='inner')
    if sf_join.num_rows() < subgraph.edges.num_rows():
        subgraph_flag = False

    return subgraph_flag

## Use the function on a toy example
g = gl.SGraph().add_vertices([gl.Vertex(i) for i in range(3)])
g = g.add_edges([gl.Edge(0, 1), gl.Edge(0, 2)])

g2 = gl.SGraph().add_vertices([gl.Vertex(i) for i in range(3)])
g2 = g2.add_edges(gl.Edge(0, 1))
print is_subgraph(g2, g)
# True

g2 = g2.add_edges(gl.Edge(1, 2))
print is_subgraph(g2, g)
# False
