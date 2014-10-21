# You need the following package for this
# Installation : pip install pillow
# Source : http://pillow.readthedocs.org/en/latest/index.html
import PIL.Image
import graphlab as gl
import  urllib2 as urllib
import io




_format = {'JPG': 0, 'PNG': 1, 'RAW': 2, 'UNDEFINED': 3}

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
    format_enum = _format['RAW']
    image_data_size = len(image_data)

    # Construct a graphlab.Image

    img = gl.Image(_image_data=image_data, _width=width, _height=height, _channels=channels, _format_enum=format_enum, _image_data_size=image_data_size)
    return img

# Sample conversion

# Retrive image from the web
fd = urllib.urlopen("http://s3.amazonaws.com/gl-testdata/images/sample.jpg")
image_file = io.BytesIO(fd.read())

# Convert from PIL to graphlab
pil_img = PIL.Image.open(image_file)
gl_img = from_pil_image(pil_img)

