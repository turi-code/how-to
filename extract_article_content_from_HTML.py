# Be sure to install boilerpipe (pip install boilerpipe)
"""
Extract main article content from HTML with Boilerpipe

In this script, we define a function that takes a single HTML news article as
input and returns the primary textual content of the article. We create an
SFrame from a sample of HTML articles, and then we pass the function defined
above to the apply method on the column in our SFrame containing the HTML
source. The clean content is included in our SFrame as a new column. We use the
Python boilerpipe module to extract the clean text.
"""
import graphlab as gl
import os
import requests
from StringIO import StringIO
from urllib import urlopen
from zipfile import ZipFile

def extract_article_content(src_content):
    """
    Extract the primary textual content from an HTML news article.

    In many cases, the HTML source of news articles is littered with boilerplate
    text that you would not want to include when doing text analysis on the
    content the page. Even if you could write some rules to extract the content
    from one page, it's unlikely that those rules would apply to an article from
    another site. The boilerpipe module allows us to solve this problem more
    generally.

    Parameters
    ----------
    src_conent : str
        The source HTML from which to extract the content.

    Returns
    -------
    out : str
        The primary content of the page with all HTML and boilerplate text
        removed.

    Examples
    --------
    >>> extract_article_content(
            "<html><body><p>Dato is in the business of building the best " \
            "machine learning platform on the planet. Our goal is to make it " \
            "easy for data scientists to build intelligent, predictive " \
            "applications quickly and at scale. Given the perplexing array " \
            "of tools in this space, we often get asked "Why Dato? What " \
            "differentiates it from tools X, Y, and Z?" This blog post aims " \
            "to provide some answers. I’ll go into some technical details " \
            "about the challenges of building a predictive application, and " \
            "how Dato’s ML platform can help.</p></body></html>")


    See Also
    --------
    - `Boilerpipe project <https://code.google.com/p/boilerpipe/>`_
    - `Boilerpipe Python module <https://pypi.python.org/pypi/boilerpipe>`_
    """
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
