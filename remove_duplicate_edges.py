import graphlab as gl

vertices = gl.SFrame({'id':[1,2,3,4,5]})
edges = gl.SFrame({'src':[1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4],
                   'dst':[2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5]})
edges['edata'] = edges['src'] + edges['dst']

# Create a graph (as an example)
g = gl.SGraph(vertices, edges, vid_field='id', src_field='src', dst_field='dst')
print g.summary()
print g.vertices
print g.edges

# Remove duplicates
g2 = gl.SGraph(g.vertices, g.edges.groupby(['__src_id', '__dst_id'], 
                                {'data': gl.aggregate.SELECT_ONE('edata')}))
print g2.summary()
print g2.vertices
print g2.edges
