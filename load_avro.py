# Load Avro formated file into an SFrame
import graphlab as gl
import os

def load_sframe_from_avro(url):
    """
    Load data from an Avro file into an SArray, and then transform it such that
    each root-level field in the Avro schema corresponds to a column in your
    SFrame.

    @input filename Name of the file to be read.
    @returns Output SFrame
    """
    # download an Avro file from S3
    gl.util.download_dataset(url, extract=False)

    # load the downloaded Avro file into an SArray
    my_avro_file = os.path.basename(url)
    sf = gl.SArray.from_avro(my_avro_file).unpack()

    # rename column names after unpack
    sf.rename({cn: cn[2:] for cn in sf.column_names()})

    """
    >>> sf.head(1)
    Columns:
        business_id	str
        date	str
        review_id	str
        stars	int
        text	str
        type	str
        user_id	str
        votes	dict

    Rows: 1

    Data:
    +------------------------+------------+------------------------+-------+
    |      business_id       |    date    |       review_id        | stars |
    +------------------------+------------+------------------------+-------+
    | WIcDFpHEnC3ihNmS7-6-ZA | 2011-02-11 | 0ESSqLfOae77muWTv_zUqA |   3   |
    +------------------------+------------+------------------------+-------+
    +--------------------------------+--------+------------------------+
    |              text              |  type  |        user_id         |
    +--------------------------------+--------+------------------------+
    | Lately i have been feeling ... | review | r-t7IiTSD0QZdt8lOUCqeQ |
    +--------------------------------+--------+------------------------+
    +--------------------------------+
    |             votes              |
    +--------------------------------+
    | {'funny': 1, 'useful': 1,  ... |
    +--------------------------------+
    [1 rows x 8 columns]
    """

    return sf

avro_sf = load_sframe_from_avro(
    'https://s3.amazonaws.com/GraphLab-Datasets/how-to/reviews.avro')
