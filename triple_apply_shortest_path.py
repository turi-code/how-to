import graphlab as gl
import time

def sssp_update_fn(src, edge, dst):
    sdist = src['distance']
    ddist = dst['distance']
    if sdist + 1 < ddist:
        dst['changed'] = True
        dst['distance'] = sdist + 1
    return (src, edge, dst)

def sssp_triple_apply(input_graph, src_vid, max_distance=1e30):
    g = gl.SGraph(input_graph.vertices, input_graph.edges)
    g.vertices['distance'] = \
      g.vertices['__id'].apply(lambda x: max_distance if x != src_vid else 0.0)
    it = 0
    num_changed = len(g.vertices)
    start = time.time()
    while(num_changed > 0):
        g.vertices['changed'] = 0
        g = g.triple_apply(sssp_update_fn, ['distance', 'changed'])
        num_changed = g.vertices['changed'].sum()
        print 'Iteration %d: num_vertices changed = %d' % (it, num_changed)
        it = it + 1
    print 'Triple apply sssp finished in: %f secs' % (time.time() - start)
    return g

# Load graph
g = gl.load_graph('http://snap.stanford.edu/data/email-Enron.txt.gz', 'snap')

# Run triple apply sssp
triple_apply_sssp_distance = sssp_triple_apply(g, src_vid=0)
print triple_apply_sssp_distance
