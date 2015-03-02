# Extract article content from HTML with Boilerpipe
# Be sure to install boilerpipe (pip install boilerpipe)
import graphlab as gl
import codecs
import os
import requests
import subprocess
from StringIO import StringIO
from urllib import urlopen
from zipfile import ZipFile

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

# Create SArray of filenames and read content of each file into SFrame
with ZipFile(StringIO(urlopen(source_s3_path).read())) as z:
    source_sa = gl.SArray([f for f in z.namelist() if not os.path.isdir(f) and f.endswith(".html")])
    dataset = gl.SFrame({"source": source_sa.apply(lambda f: z.open(f).read())})

# Extract clean text for each HTML file and create new column caled "content"
dataset["content"] = dataset["source"].apply(
    lambda src: (extract_article_content(src) or None) if src else None)

# Columns:
# 	source	str
# 	content	str

# Rows: 1000

# Data:
# +-------------------------------+-------------------------------+
# |             source            |            content            |
# +-------------------------------+-------------------------------+
# | <!DOCTYPE html PUBLIC "-//... | My good friend from colleg... |
# | <!DOCTYPE html PUBLIC "nul... | Honda "Hackura": un auto, ... |
# | <!DOCTYPE html>\n\n\n<!--[... |              None             |
# | <!DOCTYPE html PUBLIC "-//... | The Monad is like a bellow... |
# | <!DOCTYPE html>\n<html lan... | Need help cloning? Visit B... |
# | <!DOCTYPE html>\n\n\n<!--[... |              None             |
# | <!DOCTYPE html>\r\n<!--[if... | Should I Become an Entrepr... |
# | <!DOCTYPE HTML PUBLIC "-//... | Posted by Mikko @ 11:51 GM... |
# | <HTML>\n\n<head>\n<!-- red... | Why Did Human History Unfo... |
# | \n<!-- Our standard header... | Remember selection for thi... |
# |              ...              |              ...              |
# +-------------------------------+-------------------------------+
# [1000 rows x 2 columns]
# Note: Only the head of the SFrame is printed.
# You can use print_rows(num_rows=m, num_columns=n) to print more rows and columns.
