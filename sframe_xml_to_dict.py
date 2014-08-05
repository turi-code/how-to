# You need the following package for this
# Installation : pip install xmldict
# Source       : https://github.com/thoughtnirvana/xmldict
import xmldict
import graphlab as gl

def xml_filename_to_dict(filename):
    """
    Reads the contents of an XML file, parses it and returns a dictionary.

    Args:
      filename: The name of the file with xml contents.
    Returns:
      A dictionary with the contents of the xml file.

    >>> xml_filename_to_dict('file-1.xml')
    {'foo': 'bar'}

    """

    # Step 1: Read the contents of the file into a string
    f = open(filename).readlines()
    fstring = '\n'.join(f)

    # Step 2: Convert the contents of the XML file into a dictionary
    return xmldict.xml_to_dict(fstring)


# Let us assume that you have a set of files in the file "all_files.csv"
# Sample contents (of all_files.csv)
# 
# file-1.xml
# file-2.xml
# ...
# 
# file-200.xml

# Read the names of the files in to an SFrame
all_files = gl.SFrame.read_csv('all_files.csv', header=False)
all_files.rename({'X1': 'filename'})

# Parse contents of xml files into a dictionary and update the SFrame 
# with the data (one xml file per row)
data = gl.SFrame()
data['xml-dictionary'] = all_files['filename'].apply(lambda x: xml_filename_to_dict(x))

