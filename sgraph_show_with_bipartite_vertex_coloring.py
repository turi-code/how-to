# Show an SGraph with bipartite vertex coloring
import graphlab as gl

# Import the actors/films graph as used in https://dato.com/learn/gallery/notebooks/graph_analytics_movies.html
sf = gl.SFrame.read_csv('https://s3.amazonaws.com/dato-datasets/americanMovies/freebase_performances.csv', column_type_hints={'year': int})

# Filter to just the movies that certain actors have been in
sf = sf[(sf['actor_name'] == 'Matt Damon') | \
        (sf['actor_name'] == 'Ben Affleck') | \
        (sf['actor_name'] == 'Brad Pitt') | \
        (sf['actor_name'] == 'George Clooney')]

# Build a bipartite graph (actors -> movies)
sg = gl.SGraph().add_edges(sf, src_field='actor_name', dst_field='film_name')

# Highlight the actors in the graph
sg.show(vlabel='__id', vlabel_hover=True, highlight=list(sf['actor_name'].unique()))
