# Contributing to graphlab-code/how-to

A how-to is a small code snippet (roughly 2-15 lines of actual code) that shows
how to accomplish a specific task with GraphLab Create. It may include the use
of other Python packages (such as Pandas, matplotlib, etc.) when relevent. The
content of a how-to should be an example of something that is not obvious to
someone experienced in Python (like getting the length of an object), but not
too complex as to warrant a larger piece (blog post, user guide chapter, etc.).

## Contributor guidelines

### License

All contents of pull requests must conform to the [CC0 1.0 Universal](LICENSE)
license. Any changes submitted will be licensed under this license.

### Content and style guidelines

How-to examples should consist of code and comments in a .py file.

* The whole .py file should be runnable as a program. The code should not rely on any implicit or global state.
* When possible, datasets that are used should be accessible via a public (http or S3) URL or synthetically created in the example.
* When importing graphlab, import graphlab as gl.
* All required external (non-GraphLab Create and non-builtin) Python packages should have a comment at the top, to direct the user how to install:
  
  ```python
  # Requires 'pip install python-dateutil==1.5'
  ```
* Use capital letters at the beginning of each comment. Punctuation at the end is not required.
* Use a comment to explain the presence of any [magic number](http://en.wikipedia.org/wiki/Magic_number_(programming))

## New how-tos

We welcome suggestions for new how-to examples for GraphLab Create. Please
submit a pull request. The guidelines for writing how-to examples apply.
Additionally, please add a link to the [readme](README.md) with a title and a
link to your example. If the how-to does not fit into one of the categories
already present, then please add a new category.

## Changes to existing how-tos

We welcome pull requests for changes to existing how-tos. Such a change should
ideally make the example more clear, more correct, and/or simpler. 
