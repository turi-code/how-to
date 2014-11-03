import graphlab as gl

# Construct list of URLS
url_list = ['http://s3.amazonaws.com/gl-testdata/images/sample.jpg','http://s3.amazonaws.com/gl-testdata/images/sample.png']

# Construct SArry of urls
url_sarray = gl.SArray(url_list)

# Construct SArray of Images
image_sarray = url_sarray.apply(lambda x: gl.Image(x))
