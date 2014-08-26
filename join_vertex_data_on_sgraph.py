import graphlab as gl

# Load graph
g = gl.load_graph('http://snap.stanford.edu/data/email-Enron.txt.gz', 'snap')

# Compute various graph statistics
pagerank_model = gl.pagerank.create(g)
pagerank_graph = pagerank_model['graph']
print pagerank_graph.vertices

triangle_counting_model = gl.triangle_counting.create(g)
triangle_counting_graph = triangle_counting_model['graph']
print triangle_counting_graph.vertices

# Joined the computed statistics in a new graph
v = pagerank_graph.vertices.join(triangle_counting_graph.vertices)
joined_graph = gl.SGraph(v, g.edges)
print joined_graph.vertices
