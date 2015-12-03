import graphlab as gl

def get_word_frequency(docs):
  """
  Returns the frequency of occurrence of words in an SArray of documents
  Args:
    docs: An SArray (of dtype str) of documents
  Returns:
    An SFrame with the following columns:
     'word'      : Word used
     'count'     : Number of times the word occured in all documents.
     'frequency' : Relative frequency of the word in the set of input documents.
  """

  # Use the count_words function to count the number of words.
  docs_sf = gl.SFrame()
  docs_sf['words'] = gl.text_analytics.count_words(docs)

  # Stack the dictionary into individual word-count pairs.
  docs_sf = docs_sf.stack('words', 
                         new_column_name=['word', 'count'])

  # Count the number of unique words (remove None values)
  docs_sf = docs_sf.groupby('word', {'count': gl.aggregate.SUM('count')})
  docs_sf['frequency'] = docs_sf['count'] / docs_sf["count"].sum()
  return docs_sf

# Sample SArray
docs = gl.SArray(['The quick', 'brown fox', 
                         'jumps over the', 'lazy dog'])
docs_count = get_word_frequency(docs)
print docs_count

# +-------+-------+-----------+
# |  word | count | frequency |
# +-------+-------+-----------+
# | brown |   1   |    0.25   |
# |  lazy |   1   |    0.25   |
# |  dog  |   1   |    0.25   |
# | quick |   1   |    0.25   |
# | jumps |   1   |    0.25   |
# |  the  |   2   |    0.5    |
# |  fox  |   1   |    0.25   |
# |  over |   1   |    0.25   |
# +-------+-------+-----------+
