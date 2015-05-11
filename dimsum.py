import graphlab as gl
import random
import numpy as np
import time

def dimsum(A, similarity_threshold=0.1):
    """
    Compute an approximate A^T A for sparse A using the DIMSUM algorithm.

    Parameters
    ----------
    A : SFrame
      An SFrame with three columns representing the nonzero elements of a
      sparse matrix:
        * first column (of type int) represents the row id
        * second column (of type int) represents the column id
        * third column (of type float) represents the value at that element

    similarity_threshold : float
      This governs roughly how many nonzero elements to return in the result.

    Returns
    -------
    out : SFrame
      An SFrame having columns item_id_a and the nearest items, item_id_b,
      along with the estimated similarity.

    References
    ----------
    https://blog.twitter.com/2014/all-pairs-similarity-via-dimsum
    """

    assert A.num_cols() == 3
    (row_name, col_name, val_name) = A.column_names()

    # Compute norms of each column
    A['sqval'] = A[val_name] * A[val_name]
    ssq = A.groupby(col_name, {'c': gl.aggregate.SUM('sqval')})
    ssq['c'] = ssq['c'].apply(lambda x: np.sqrt(x))
    c = ssq.unstack([col_name, 'c'], new_column_name='d')['d'][0]
    del A['sqval']

    # Compute the suggested tuning parameter gamma
    m = A[row_name].max()
    n = A[col_name].max()
    sqrt_gamma = np.sqrt(4 * np.log(n) / similarity_threshold)

    # Rearrange to be adjacency list format
    adjlist = A.unstack([col_name, val_name], 'r_i')

    def mapper(r_i):
        emit = {}
        for j, a_ij in r_i.iteritems():
            prob_j = min(1.0, sqrt_gamma / c[j])
            if random.random() < prob_j:
                for k, a_ik in r_i.iteritems():
                    prob_k = min(1.0, sqrt_gamma / c[k])
                    if random.random() < prob_k:
                        key = str(j) + '_' + str(k)
                        val = a_ij * a_ik /           \
                              min(sqrt_gamma, c[j]) / \
                              min(sqrt_gamma, c[k])
                        emit[key] = val
        return emit

    # Perform map
    adjlist['emit'] = adjlist['r_i'].apply(mapper)

    # Limit to jobs that returned non-zero results
    adjlist['num_emit'] = adjlist['emit'].apply(len)
    emitted = adjlist[['emit']][adjlist['num_emit'] > 0]

    # Perform reduce
    edges  = emitted.stack('emit')\
                    .groupby('X1', {'similarity': gl.aggregate.SUM('X2')})

    # Rearrange to three columns
    edges[col_name + '_a'] = edges['X1'].apply(lambda x: x.split('_')[0]).astype(int)
    edges[col_name + '_b'] = edges['X1'].apply(lambda x: x.split('_')[1]).astype(int)

    # Sort
    edges = edges[[col_name + '_a', col_name + '_b', 'similarity']]
    edges = edges.sort('similarity', ascending=False)

    return edges

if __name__ == "__main__":

    # Prepare the data to be an SFrame with three columns. The ml-20m dataset
    # can be obtained here http://grouplens.org/datasets/movielens/
    ratings = gl.SFrame.read_csv('ml-20m/ratings.csv')
    ratings = ratings.head(5000000)
    movies = gl.SFrame.read_csv('ml-20m/movies.csv')
    del ratings['timestamp']

    # Method suggests that values are 0-centered.
    ratings['rating'] = ratings['rating'] - ratings['rating'].mean()

    # Compute approximate A^T * A.
    start_time = time.time()
    ata = dimsum(ratings, .5)  # smaller thresholds require more time.
    print time.time() - start_time

    ata = ata[ata['movieId_a'] != ata['movieId_b']]

    # Visually inspect whether we get similar movies
    sim = ata.join(movies, on={'movieId_a': 'movieId'})\
             .join(movies, on={'movieId_b': 'movieId'})

    chosen = ['European Vacation (1985)',
              'Good Morning Vietnam (1987)',
              'Lethal Weapon 3 (1992)' ,
              'Batman Forever (1995)', 'Congo (1995)']
    for c in chosen:
        sim[sim['title'] == c].print_rows(max_row_width=200)

