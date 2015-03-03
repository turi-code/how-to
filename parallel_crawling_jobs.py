"""
Launch parallel jobs in EC2 for crawling web pages linked from Hacker News posts

In this script, we define two top-level functions with the primary crawling
logic, which will be distributed among a few worker nodes in EC2. The content of
each page crawled is written to S3. We also define a utility function for
dividing the data set as evenly as possible. The remainder of the script is job
configuration logic.

We use the requests module for requesting HTML pages and the boto module for
writing to Amazon S3.
"""
import graphlab as gl

@gl.deploy.required_packages(["requests == 2.3.0", "boto == 2.33.0"])
def get_source(s3_bucket, s3_save_path, _id, url):
    """
    Crawl a page given a URL and write the page source to S3.

    Parameters
    ----------
    s3_bucket : str or boto.s3.bucket.Bucket
        The name of the bucket to which the HTML source will be written. The
        caller must have write access to this bucket.

    s3_save_path : str
        A path prefix to append to the S3 key that will be created (eg.
        "my_data/html".

    _id : int
        The identifier for the page, which will be used as the S3 key name (eg.
        "12345.html").

    url : str
        The URL for the page to crawl.

    Examples
    --------
        >>> get_source("my_bucket", "data/html", 12345,
                       "http://blog.dato.com/the-challenges-of-building-" \
                       "the-next-gen-machine-learning-platform")
    """
    import requests
    import logging
    import boto
    from boto.s3.connection import S3Connection

    if not isinstance(s3_bucket, boto.s3.bucket.Bucket):
        s3_bucket = S3Connection().get_bucket(s3_bucket)
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response_txt = response.text
        full_path = s3_save_path + "/%s.html" % _id
        s3_key = s3_bucket.new_key(full_path)
        s3_key.set_contents_from_string(response_txt)
        return full_path
    except requests.exceptions.Timeout:
        logging.getLogger().warning("Request for (%s, %d) timed out" % (url, _id))
    except Exception as e:
        logging.getLogger().warning("Unexpected error on article (%s, %d): %s" % (url, _id, e.message))

@gl.deploy.required_packages(["boto == 2.33.0"])
def get_all_source(s3_bucket, s3_save_path, id_url_pairs):
    """
    Crawl all pages specified in id_url_pairs and write to the S3 path specified
    by s3_bucket/s3_save_path.

    Parameters
    ----------
    s3_bucket : str or boto.s3.bucket.Bucket
        The name of the bucket to which the HTML source will be written. The
        caller must have write access to this bucket.

    s3_save_path : str
        A path prefix to append to the S3 key that will be created (eg.
        "my_data/html".

    id_url_pairs : list of (int, str) pairs
        A list of pairs containing an integer page ID and a page URL, for each
        URL to be crawled.
    """
    import boto
    from boto.s3.connection import S3Connection

    results = []

    if not isinstance(s3_bucket, boto.s3.bucket.Bucket):
        s3_bucket = S3Connection().get_bucket(s3_bucket)

    for _id, url in id_url_pairs:
        results.append(get_source(s3_bucket, s3_save_path, _id, url))

    return results

# Divvy up a list of items as evenly as possible into n lists
def divvy(items, n):
    q, r = divmod(len(items), n)
    indices = [q * i + min(i, r) for i in xrange(n + 1)]
    return [items[indices[i]:indices[i + 1]] for i in xrange(n)]

# Load Hacker News metadata SFrame from S3
stories_sf = gl.load_sframe("s3://dato-datasets/hacker_news/stories.sframe")

# Get a list of ID, URL pairs from SFrame
id_url_pairs = [(x["id"], x["url"]) for x in stories_sf if x["url"]]

# Divvy the list of ID, URL pairs from above and pass to n=4 workers
chunks = divvy(id_url_pairs, 4)

# The S3 bucket and path to where source articles are to be stored in S3
# Set this to a bucket to which you have write access
s3_bucket = "my-bucket"
s3_save_path = "hacker_news/source_html"

# Specify EC2 execution environment
# The 2nd parameter should be set to an S3 bucket to which you will write logs
ec2 = gl.deploy.environment.EC2("ec2", "s3://my-bucket/logs")

# Launch 4 jobs
for chunk in chunks:
    gl.deploy.job.create(lambda: get_all_source(s3_bucket, s3_save_path, chunk),
                         environment=ec2, num_hosts=1, name="get_all_source")
