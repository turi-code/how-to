# Launch parallel jobs in EC2 for crawling web pages
import graphlab as gl
import functools

# Load Hacker News metadata SFrame from S3
stories_sf = gl.load_sframe("s3://dato-datasets/hacker_news/stories.sframe")

# Get a list of ID, URL pairs from SFrame
id_url_pairs = [(x["id"], x["url"]) for x in stories_sf if x["url"]]

# The base path to where source articles are to be stored in S3
s3_base_path = "s3://my-bucke/hacker_news/source_html"

# Define a function to be called for each ID, URL pair
@gl.deploy.required_packages(['requests == 2.3.0'])
def get_source(id, url, s3_base_path, timeout=10):
    import requests
    import logging
    import codecs
    from graphlab.deploy._predictive_service._file_util import upload_to_s3

    try:
        response_txt = requests.get(url, timeout=timeout).text
        filename = "%d.html" % id
        with codecs.open(filename, "w", "utf8") as f:
            f.write(response_txt)
        s3_path = s3_base_path + "/" + filename
        upload_to_s3(filename, s3_path)
        return s3_path
    except requests.exceptions.Timeout:
        logging.getLogger().warning("Request for (%s, %d) timed out" % (url, id))
    except Exception as e:
        logging.getLogger().warning("Unexpected error on article (%s, %d): %s" % (url, id, e.message))

# Divvy up the list of ID, URL pairs to distribute among 4 workers
def divvy(items, n):
    q, r = divmod(len(items), n)
    indices = [q * i + min(i, r) for i in xrange(n + 1)]
    return [items[indices[i]:indices[i + 1]] for i in xrange(n)]

chunks = divvy(id_url_pairs, 4)

# Define a top-level function to get all source for all ID, URL pairs
def get_all_source(id_url_pairs):
    results = []
    for _id, url in id_url_pairs:
        results.append(get_source(_id, url, s3_base_path))
    return results

# Specify EC2 execution environment
ec2 = gl.deploy.environment.EC2("ec2", "s3://my-bucket/logs")

# Launch 4 jobs
for chunk in chunks:
    gl.deploy.job.create(functools.partial(get_all_source, chunk),
                         environment=ec2, num_hosts=1, name="get_all_source")
