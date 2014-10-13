# Title : Convert a graphlab Image to a PIL Image, rotate it, and convert it back
# to a Graphlab Image. Use the apply function to rotate all images in an SFrame.

# You need the following package for this
# Installation : pip install pillow
# Source : http://pillow.readthedocs.org/en/latest/index.html
from PIL import Image as PIL_image
import graphlab as gl
import StringIO as _StringIO

JPG = "JPG"
PNG = "PNG"
RAW = "RAW"
UNDEFINED = "UNDEFINED"


CURRENT_VERSION = 0

_format = {JPG: 0, PNG: 1, RAW: 2, UNDEFINED: 3}

def from_pil_image(pil_img):
    """
    Returns a graphlab.Image constructed from the passed PIL Image

    Parameters
    ----------
        pil_img : PIL.Image
            A PIL Image that is to be converted to a graphlab.Image

    Returns
    --------
        out: graphlab.Image
            The input converted to a graphlab.Image
    """
    # Read in PIL image data and meta data
    height = pil_img.size[1]
    width = pil_img.size[0]
    if pil_img.mode == 'L':
        image_data = bytearray([z for z in pil_img.getdata()])
        channels = 1
    elif pil_img.mode == 'RGB':
        image_data = bytearray([z for l in pil_img.getdata() for z in l ])
        channels = 3
    else:
        image_data = bytearray([z for l in pil_img.getdata() for z in l])
        channels = 4
    format_enum = _format[RAW]
    image_data_size = len(image_data)

    # Construct a graphlab.Image

    img = gl.Image(_image_data=image_data, _width=width, _height=height, _channels=channels, _format_enum=format_enum, _image_data_size=image_data_size, _version=CURRENT_VERSION)
    return img

def to_pil_image(gl_img):
    """
    Returns a PIL Image constructed from the passed graphlab.Image

    Parameters
    ----------
        gl_img : graphlab.Image
            A graphlab.Image that is to be converted to a PIL Image

    Returns
    -------
        out : PIL.Image
            The input converted to a PIL Image
    """
    if gl_img._format_enum == _format[RAW]:
        # Read in Image, switch based on number of channels.
        if gl_img.channels == 1:
            img = PIL_image.frombytes('L', (gl_img._width, gl_img._height), str(gl_img._image_data))
        elif gl_img.channels == 3:
            img = PIL_image.frombytes('RGB', (gl_img._width, gl_img._height), str(gl_img._image_data))
        elif gl_img.channels == 4:
            img = PIL_image.frombytes('RGBA', (gl_img._width, gl_img._height), str(gl_img._image_data))
        else:
            raise ValueError('Unsupported channel size: ' + str(gl_img.channels))
    else:
        img = PIL_image.open(_StringIO.StringIO(gl_img._image_data))
    return img


def rotate_image(img):
    """
    Returns a graphlab.Image that takes the input image and rotates
    it 90 degrees.

    Parameters
    ----------
        img : graphlab.Image
            A graphlab.Image that is to be rotated 90 degress.

    Returns
    -------
        out : graphlab.Image
            The input image rotated 90 degrees.


    """
    pil_img = to_pil_image(img)
    pil_img = pil_img.rotate(90)
    return from_pil_image(pil_img)

# Read in SFrame of images
dataset = gl.SFrame('http://s3.amazonaws.com/GraphLab-Datasets/mnist/sframe/train6k')

#Pull out SArray
images = dataset['image']

# Rotate images
rotated = images.apply(rotate_image)

