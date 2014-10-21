import graphlab as gl


# Load the mnist data into an SArray of dtype array.array. This dataset comes from
# http://yann.lecun.com/exdb/mnist/, courtesy of Yann LeCun and Corinna Cortes.
mnist_array = gl.SArray('http://s3.amazonaws.com/GraphLab-Datasets/mnist/mnist_vec_sarray')

# The MNIST data is scaled from 0 to 1, but our image type only loads integer  pixel values
# from 0 to 255. If we just convert without scaling, all values below one would be cast to
# 0.

scaled_mnist_array = mnist_array * 255

# Now let's convert to an Sarray of image type. The images are of size 28 x 28 x 1
# (since they are grayscale). Since the scaling will still result in some non-integer
# values, we want to set allow_rounding to True.

mnist_img_sarray = gl.SArray.pixel_array_to_image(scaled_mnist_array, 28, 28, 1, allow_rounding = True)
