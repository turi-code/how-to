import graphlab as gl
import time

def pagerank_update_fn(src, edge, dst):
    if src['__id'] != dst['__id']: # ignore self-links
        dst['pagerank'] += src['prev_pagerank'] * edge['weight']
    return (src, edge, dst)

def sum_weight(src, edge, dst):
    if src['__id'] != dst['__id']: # ignore self-links
        src['total_weight'] += edge['weight']
    return src, edge, dst

def normalize_weight(src, edge, dst):
    if src['__id'] != dst['__id']: # ignore self-links
        edge['weight'] /= src['total_weight']
    return src, edge, dst

def pagerank_triple_apply(input_graph, reset_prob=0.15, threshold=1e-3, 
                          max_iterations=20):
    g = gl.SGraph(input_graph.vertices, input_graph.edges)

    # compute normalized edge weight
    g.vertices['total_weight'] = 0.0
    g = g.triple_apply(sum_weight, ['total_weight'])
    g = g.triple_apply(normalize_weight, ['weight'])
    del g.vertices['total_weight']

    # initialize vertex field
    g.vertices['prev_pagerank'] = 1.0
    it = 0
    total_l1_delta = len(g.vertices)
    start = time.time()
    while(total_l1_delta > threshold and it < max_iterations):
        g.vertices['pagerank'] = 0.0
        g = g.triple_apply(pagerank_update_fn, ['pagerank'])
        g.vertices['pagerank'] = g.vertices['pagerank'] * (1 - reset_prob) \
                                                                  + reset_prob
        g.vertices['l1_delta'] = (g.vertices['pagerank'] - \
                          g.vertices['prev_pagerank']).apply(lambda x: abs(x))
        total_l1_delta = g.vertices['l1_delta'].sum()
        g.vertices['prev_pagerank'] = g.vertices['pagerank']
        print 'Iteration %d: total pagerank changed in L1 = %f' % (it,\
                                                                total_l1_delta)
        it = it + 1
    print 'Triple apply pagerank finished in: %f secs' % (time.time() - start)
    del g.vertices['prev_pagerank']
    return g

# Load graph
g = gl.load_graph('http://snap.stanford.edu/data/email-Enron.txt.gz', 'snap')
g.edges['weight'] = 1.0

# Run triple apply sssp
pagerank_graph = pagerank_triple_apply(g)
print pagerank_graph
