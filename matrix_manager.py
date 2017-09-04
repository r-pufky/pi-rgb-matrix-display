#
# RGB Matrix interface for HAT75 devices.
#
# See: https://www.adafruit.com/product/2345
#
# Requires rgbmatrix.so library: github.com/adafruit/rpi-rgb-led-matrix
#

import atexit
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from rgbmatrix import Adafruit_RGBmatrix

class MatrixInterface(object):
  """ Provides an interface to manipulate the LED Matrix Display.

  Images are drawn in offscreen buffer, then the buffer is moved in place.
  """

  def __init__(self, matrix_size=32, chain_length=2):
    """ Initialize matrix interface.

    Args:
      matrix_size: Integer size of RGB matrix attached. Default: 32.
      chain_length: Integer number of matrix's attached. Default: 2.
    """
    self.matrix_size = matrix_size
    self.chain_length = chain_length
    # todo look into setup for veritcal screens.
    self.screen_width = matrix_size * chain_length
    self.screen_height = matrix_size
    self.matrix = Adafruit_RGBmatrix(matrix_size, chain_length)
    self.offscreen_buffer = Image.new('RGB',
                                      (self.screen_width, self.screen_height))
    self.render = ImageDraw.Draw(self.offscreen_buffer)
    self.FillScreen()

  def FillScreen(self, fill=(0,0,0)):
    """ Fills the matrix display with a given color.

    Args:
      fill: Tuple containing (Integer: R, Integer: G, Integer: B) values.
          Default: Black (0, 0, 0).
    """
    self.render.rectangle((0, 0, self.screen_width, self.screen_height),
                          fill=fill)

  def DrawScreen(self, image):
    """ Update screen buffer with new image.

    Args:
      image: Image in RGB format, constraint to matrix screen size.
    """
    if image.width != self.screen_width or image.height != self.screen_height:
      raise Exception('MatrixInterface: will not display image larger or '
                      'smaller than screen size.')
    self.offscreen_buffer = image

  def Render(self):
    """ Render screen buffer to screen."""
    self.matrix.SetImage(self.image.im.id, 0, 0)

  @atexit.register
  def TurnOffScreen(self):
    """ Clears and powers off the screen.

    Register to always call when program exits.
    """
    if self.matrix:
      self.matrix.Clear()