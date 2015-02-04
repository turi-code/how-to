import graphlab as gl

def get_vocabulary(docs):
  """
  Returns the set of unique words in an SArray of documents
  Args:
    docs: An SArray (of dtype str) of documents
  Returns:
    An SArray of unique words
  """

  # Use the count_words function to count the number of words.
  docs_sf = gl.SFrame()
  docs_sf['words'] = gl.text.count_words(docs)

  # Stack the dictionary into individual word-count pairs.
  docs_sf = docs_sf.stack('words', 
                         new_column_name=['word', 'count'])

  # Count the number of unique words (remove None values)
  corpus = docs_sf['word'].unique()
  corpus = corpus.dropna()
  return corpus

# Sample SArray
docs = gl.SArray(['The quick', 'brown fox', 
                         'jumps over the', 'lazy dog'])
corpus = get_vocabulary(docs)

