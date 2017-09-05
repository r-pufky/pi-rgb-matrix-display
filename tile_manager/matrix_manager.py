#
# RGB Matrix interface for HAT75 devices.
#
# See: https://www.adafruit.com/product/2345
#
# Requires rgbmatrix.so library: github.com/adafruit/rpi-rgb-led-matrix
#
# This library requires ROOT to access the GPIO pins. If you recieve a 
# 'SystemError: dynamic module not initialized properly' it is because you are
# not initalizing this module with root permissions.
#

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from rgbmatrix import Adafruit_RGBmatrix


class MatrixInterface(object):
  """ Provides an interface to manipulate the LED Matrix Display.

  ROOT privileges are required to access the GPIO pins.

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
    self.screen_width = matrix_size * chain_length
    self.screen_height = matrix_size
    self.matrix = Adafruit_RGBmatrix(matrix_size, chain_length)
    self.offscreen_buffer = Image.new('RGB',
                                      (self.screen_width, self.screen_height))
    self.offscreen_draw = ImageDraw.Draw(self.offscreen_buffer)
    self.FillScreen()

  def __enter__(self):
    """ Enter runtime context for matrix interface. """
    return self

  def __exit__(self, type, value, traceback):
    """ Exit runtime context for matrix interface, turn screen off. """
    self.TurnOffScreen()

  def FillScreen(self, fill=(0,0,0)):
    """ Fills the matrix display with a given color.

    Args:
      fill: Tuple containing (Integer: R, Integer: G, Integer: B) values.
          Default: Black (0, 0, 0).
    """
    self.offscreen_draw.rectangle(
        (0, 0, self.screen_width, self.screen_height),
        fill=fill)
    self.Render()

  def Render(self):
    """ Render screen buffer to screen."""
    self.matrix.SetImage(self.offscreen_buffer.im.id, 0, 0)

  def TurnOffScreen(self):
    """ Clears and powers off the screen. """
    if self.matrix:
      self.matrix.Clear()
