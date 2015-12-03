Want to contribute a GraphLab Create How-To? We welcome [pull
requests](https://github.com/graphlab-code/how-to/pulls). Please read the
[contributor
guide](https://github.com/graphlab-code/how-to/blob/master/CONTRIBUTING.md).

Want to request a new How-To or have feedback on one listed below? Please open
a Git
[issue](https://github.com/graphlab-code/how-to/issues?q=is%3Aopen+is%3Aissue)
or send us [feedback](http://dato.com/company/contact.html).

Data Ingress
-------------
* [Import data from Pandas Series/Dataframes](pandas_to_glc.py)
* [Import data from your Spark cluster](spark_to_sframe.py)
* [Import data from your databases using SQL](sql_to_sframe.py)
* [Load a JSON file into an SFrame](load_json.py)
* [Load a collection XML files into an SFrame](sframe_xml_to_dict.py)
* [Load an Avro file into an SFrame](load_avro.py)
* [Extract main article content from HTML with Boilerpipe](extract_article_content_from_HTML.py)
* [Load a Neo4j graph from a JSON file into an SGraph](sgraph_from_neo4j_json.py)

Tabular Data Transformation
-----------------------------
* [Filter/Select rows from an SFrame](select_subset_rows.py)
* [Efficiently Calculating Basic Statistics in SArray/SFrame](sarray_basic_stats.py)
* [Find the top-k rows for each value of a group variable](top_k.py)
* [Collapse multiple columns of an SFrame into a single column of type list/dict](sframe_pack.py)
* [Parse a datetime column into its components (year, month, etc.)](split_datetime_column.py)
* [Convert a column of datetime strings into UNIX timestamps](convert_column_to_timestamp.py)
* [Expand an SFrame column of type list/dict into multiple columns](sframe_unpack.py)

Graph Data Transformation
---------------------------
* [Join vertex data on SGraph](join_vertex_data_on_sgraph.py)
* [Remove duplicate edges from SGraph](remove_duplicate_edges.py)
* [Check if one SGraph is a subgraph of a second SGraph](check_subgraph.py)

Text Analytics
---------------
* [Find the unique words used in an SArray of text documents](sarray_vocabulary.py)
* [Compute word frequencies for each word in an SArray of text documents](word_frequency.py)
* [Example of making predictions using topic model parameters](predict_topic_model.py)

Image Analytics
---------------
* [Convert an SArray of URL strings to an SArray of graphlab.Image](url_to_img.py)
* [Convert an SArray of array.array to an SArray of graphlab.Image](array_to_image.py)
* [Convert a PIL.Image to a graphlab.Image](from_pil_image.py)
* [Convert a graphlab.Image to a PIL.Image](to_pil_image.py)

Graph Analytics
-----------------
* [Implement single source shortest path using triple_apply](triple_apply_shortest_path.py)
* [Implement weighted pagerank using triple_apply](triple_apply_weighted_pagerank.py)

Sparse matrices
---------------
* [Convert an SFrame into a scipy.sparse matrix](sframe_to_scipy_sparse.py)
* [Compute approximate AtA sparse matrix product using the DIMSUM algorithm](dimsum.py)

Visualization
--------------
* [Show SGraph with custom layout using vertex_positions and NetworkX](sgraph_show_with_nx_layout.py)
* [Show SGraph with bipartite vertex coloring](sgraph_show_with_bipartite_vertex_coloring.py)
* [Show SGraph with custom vertex coloring](sgraph_show_with_vertex_coloring.py)
* [Show time-series data as a line chart in Canvas](line_chart_by_date.py)

Miscellaneous
--------------
* [Run a function on the crossproduct of option values](experiment_over_parameters.py)
* [Parallel web page crawling using Dato Distributed](parallel_crawling_jobs.py)
* [Use the logging module with GraphLab Create](user_logging.py)

Code submitted through pull requests will be made available under the [CC0 1.0
Universal
license](https://github.com/graphlab-code/how-to/blob/master/LICENSE).
