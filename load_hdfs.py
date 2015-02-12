import os
import subprocess
import graphlab as gl

# Reading from HDFS into an SFrame is easy, as long as you know how to
# construct your HDFS URL and your system has java installed in a relatively
# standard way.  This how-to is meant to help if one of those two things are
# not true for you.

#### Installation-specific variables ####
# Change these variables for your HDFS setup

hdfs_url_base = None
# An example of what should be in this variable
#hdfs_url_base = 'hdfs://my.server.com:8020'

username = 'evan'

filepath = 'test.txt'

#### Construct your HDFS URL ####
# If you don't know how to get the server and port to reach your HDFS
# installation, here's a way to do it that works on CDH 5.
if hdfs_url_base is None:
    hdfs_url_base = subprocess.check_output(
            ['hdfs', 'getconf', '-confKey', 'fs.defaultFS']).rstrip()

#### Specify a Java installation (OPTIONAL) ####
# To set a specific java implementation to execute the HDFS commands, set this
# environment variable BEFORE running any GraphLab Create commands.
os.environ['GRAPHLAB_JAVA_HOME'] = '/foo/java'

sf = gl.SFrame.read_csv(hdfs_url_base + '/user/' + username + '/' + filepath); 

print sf
