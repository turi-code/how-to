import graphlab as gl

def extract_entities(sf, entities):
    '''
    Extract entities (nodes or edges) from graph data retrieved from a
    JSON file created by Neo4j.
    Args:
    sf: The sf containing 'data' column extracted from a JSON file
        created by Neo4j.
    entities: The entities to extract from sf. Can be 'nodes' or
              'relationships'.
    Returns:
        SFrame of given entities
    '''
        
    sf[entities] = sf['data'].apply(lambda data: data['graph'][entities])
    entities_sf = sf[[entities]].stack(entities, new_column_name=entities)
    entities_sf = entities_sf.unpack(entities, column_name_prefix='')
    entities_sf = entities_sf.unpack('properties', column_name_prefix='')
    
    return entities_sf

def get_sgraph_from_neo4j_json(json_filename):
    '''
    Reads a JSON file, created by Neo4j, into an SGraph.
    Args:
        json_filename: The name of the JSON file created by Neo4j.
    Returns:
        SGraph 
    '''
    
    # Load json_filename into an SFrame
    sf = gl.SFrame.read_csv(json_filename, header=False, 
                            column_type_hints=dict, verbose=False)
    
    # Extract the graph data from sf
    sf = sf.unpack('X1', column_name_prefix='')
    sf = sf[['data']].stack('data', new_column_name='data')

    # Extract nodes and edges
    nodes_sf = extract_entities(sf, 'nodes')
    edges_sf = extract_entities(sf, 'relationships')
    
    # Create the SGraph
    sgraph = gl.SGraph()
    sgraph = sgraph.add_edges(edges_sf, src_field='startNode',
                              dst_field='endNode')
    sgraph = sgraph.add_vertices(nodes_sf, vid_field='id')
    
    return sgraph

g = get_sgraph_from_neo4j_json(
        'https://s3.amazonaws.com/GraphLab-Datasets/how-to/movies.json')
print g
# SGraph({'num_edges': 20L, 'num_vertices': 12L})
