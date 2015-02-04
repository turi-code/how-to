# Import/Export data from a Spark cluster
from pyspark import SparkContext
import graphlab as gl

# In order to use this feature, you must access your RDD through PySpark 1.1+
# The user guide contains details on how to setup Spark integration
# http://dato.com/learn/userguide/index.html#Spark_Integration
sc = SparkContext('yarn-client')

# Load a spark RDD into an SFrame
spark_rdd = sc.textFile("hdfs://my_file.csv")
sframe = gl.SFrame.from_rdd(spark_rdd)

# Perform your operations
sframe = sframe.dropna()

# Convert an SFrame to a Spark RDD
out_rdd = sf.to_rdd(sframe)
