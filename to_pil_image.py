# You need the following package for this
# Installation : pip install pillow
# Source : http://pillow.readthedocs.org/en/latest/index.html
import PIL.Image
import graphlab as gl
import StringIO as _StringIO


_format = {'JPG': 0, 'PNG': 1, 'RAW': 2, 'UNDEFINED': 3}

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
    if gl_img._format_enum == _format['RAW']:
        # Read in Image, switch based on number of channels.
        if gl_img.channels == 1:
            img = PIL.Image.frombytes('L', (gl_img._width, gl_img._height), str(gl_img._image_data))
        elif gl_img.channels == 3:
            img = PIL.Image.frombytes('RGB', (gl_img._width, gl_img._height), str(gl_img._image_data))
        elif gl_img.channels == 4:
            img = PIL.Image.frombytes('RGBA', (gl_img._width, gl_img._height), str(gl_img._image_data))
        else:
            raise ValueError('Unsupported channel size: ' + str(gl_img.channels))
    else:
        img = PIL.Image.open(_StringIO.StringIO(gl_img._image_data))
    return img

# Sample conversion
gl_img = gl.Image('http://s3.amazonaws.com/gl-testdata/images/sample.jpg')
pil_img = to_pil_image(gl_img)

