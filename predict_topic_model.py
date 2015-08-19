import numpy as np
import graphlab as gl

def predict(document_bow, word_topic_counts, topic_counts, vocab,
            alpha=0.1, beta=0.01, num_burnin=5):
    """
    Make predictions for a single document.

    Parameters
    ----------
    document_bow : dict
        Dictionary with words as keys and document frequencies as counts.

    word_topic_counts : numpy array, num_vocab x num_topics
        Number of times a given word has ever been assigned to a topic.

    topic_counts : numpy vector of length num_topics
        Number of times any word has been assigned to a topic.

    vocab : dict
        Words are keys and unique integer is the value.

    alpha : float
        Hyperparameter. See topic_model docs.

    beta : float
        Hyperparameter. See topic_model docs.

    num_burnin : int
        Number of iterations of Gibbs sampling to perform at predict time.

    Returns
    -------
    out : numpy array of length num_topics
        Probabilities that the document belongs to each topic.

    """
    num_vocab, num_topics = word_topic_counts.shape

    # proportion of each topic in this test doc
    doc_topic_counts = np.zeros(num_topics)
    # Assignment of each unique word
    doc_topic_assignments = []

    # Initialize assignments and counts
    # NB: we are assuming document_bow doesn't change.
    for i, (word, freq) in enumerate(document_bow.iteritems()):
        if word not in vocab:  # skip words not present in training set
            continue
        topic = np.random.randint(0, num_topics-1)
        doc_topic_assignments.append(topic)
        doc_topic_counts[topic] += freq

    # Sample topic assignments for the test document
    for burnin in range(num_burnin):
        for i, (word, freq) in enumerate(document_bow.iteritems()):
            if word not in vocab:
                continue
            word_id = vocab[word]

            # Get old topic and decrement counts
            topic = doc_topic_assignments[i]
            doc_topic_counts[topic] -= freq

            # Sample a new topic
            gamma = np.zeros(num_topics)  # store probabilities
            for k in range(num_topics):
                gamma[k] = (doc_topic_counts[k] + alpha) * (word_topic_counts[word_id, k] + beta) / (topic_counts[k] + num_vocab * beta)
            gamma = gamma / gamma.sum()  # normalize to probabilities
            topic = np.random.choice(num_topics, 1, p=gamma)

            # Use new topic to increment counts
            doc_topic_assignments[i] = topic
            doc_topic_counts[topic] += freq

    # Create predictions
    predictions = np.zeros(num_topics)
    total_doc_topic_counts = doc_topic_counts.sum()
    for k in range(num_topics):
        predictions[k] = (doc_topic_counts[k] + alpha) / (total_doc_topic_counts + num_topics * alpha)
    return predictions / predictions.sum()


if __name__ == '__main__':
    docs = gl.SFrame({'text': [{'first': 5, 'doc': 1}, {'second': 3, 'doc': 5}]})
    m = gl.topic_model.create(docs)

    # Get test document in bag of words format
    document_bow = docs['text'][0]

    # Input: Global parameters from trained model

    # Number of times each word in the vocabulary has ever been assigned to topic k (in any document). You can make an approximate version of this by multiplying m['topics'] by some large number (e.g. number of tokens in corpus) that indicates how strong you "believe" in these topics. Make it into counts by flooring it to an integer.
    prior_strength = 1000000
    word_topic_counts = np.array(m['topics']['topic_probabilities'])
    word_topic_counts = np.floor(prior_strength * word_topic_counts)

    # Number of times any word as been assigned to each topic.
    topic_counts = word_topic_counts.sum(0)

    # Get vocabulary lookup
    num_topics = m['num_topics']
    vocab = {}
    for i, w in enumerate(m['topics']['vocabulary']):
        vocab[w] = i
    num_vocab = len(vocab)

    # Make prediction on test document
    probs = predict(document_bow, word_topic_counts, topic_counts, vocab)
