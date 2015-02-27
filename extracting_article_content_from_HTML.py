# Extract article content from HTML with Boilerpipe
# Be sure to install boilerpipe (pip install boilerpipe)
import graphlab as gl
import codecs
import os
import subprocess

# Define function to return clean content given HTML source as string
def extract_article_content(src_content):
    import logging
    from boilerpipe.extract import Extractor

    if src_content and src_content.strip():
        try:
            extractor = Extractor(extractor='ArticleExtractor', html=src_content)
            return extractor.getText()
        except Exception as e:
            logging.getLogger().error("Exception (%s) extracting from (%s)" % \
                                      (e.message, src_content[0:25]))

# Get the sample source data
source_s3_path = "https://s3.amazonaws.com/dato-datasets/how-to/html_source_sample.zip"
subprocess.check_call(["wget", source_s3_path])
subprocess.check_call(["unzip", "html_source_sample.zip"])

# Create SArray of filenames
source_dir = "html_source_sample"
source_sa = gl.SArray([x for x in os.listdir(source_dir) if x.endswith(".html")])

# Read source HTML info SArray
dataset = gl.SFrame({"filename": source_sa,
                     "source": source_sa.apply(
                         lambda filename: codecs.open(
                             os.path.join(source_dir, filename), "r", "utf8").read())})

# Extract clean text for each HTML file and create new column caled "content"
dataset["content"] = dataset["source"].apply(
    lambda src: (extract_article_content(src) or None) if src else None)

dataset
