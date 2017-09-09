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
try:
  from rgbmatrix import Adafruit_RGBmatrix
except ImportError as e:
  raise ImportError('\n\n\nrgbmatrix.so NOT DETECTED, ABORTING. %s\n\n' % e)


class MatrixInterface(object):
  """ Provides an interface to manipulate the LED Matrix Display.

  ROOT privileges are required to access the GPIO pins.

  Images are drawn in offscreen buffer, then the buffer is moved in place.
  """

  def __init__(self, matrix_size=32, chain_length=2, write_cycles=2):
    """ Initialize matrix interface.

    matrix_size and chain_length should correspond to --led-rows and
    --led-chain options from demo rgbmatrix code. This is essentially the
    size of your matrix panel and the number of panels that are chained
    together.

    Args:
      matrix_size: Integer size of RGB matrix panel attached. Default: 32.
      chain_length: Integer number of matrix's attached. Default: 2.
      write_cycles: Integer write cycle speed, higher is slower. This helps to
          mitigate flickering if present on the matrix. Standard values for
          Pi 1: 1, Pi 2/3: 2. Default: 2.
    """
    self.matrix_size = matrix_size
    self.chain_length = chain_length
    self.screen_shape = self.GetMatrixShape()
    self.screen_width = len(self.screen_shape[0]) * self.matrix_size
    self.screen_height = len(self.screen_shape) * self.matrix_size

    self.matrix = Adafruit_RGBmatrix(matrix_size, chain_length)
    self.matrix.SetWriteCycles(write_cycles)

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

  def GetMatrixShape(self):
    """ Returns an array representing the shape of the matrix display.

    The screen must always form to be a rectangle in all assembled cases.

    This is calculated based on the data from the RGB Matrix library and some
    additional testing, per: https://github.com/hzeller/rpi-rgb-led-matrix:

    Type    Scan  Multiplexing   Program Option  Remark
    128x128 ?     --led-rows=64  --led-chain=4   *
    64x64   1:32  --led-rows=64  --led-chain=2   For displays with E line. (32x32)
    128x32  ?     --led-rows=32  --led-chain=4   *internally four chained 32x32
    96x32   ?     --led-rows=32  --led-chain=3   *internally three chained 32x32
    64x32   1:16  --led-rows=32  --led-chain=2   internally two chained 32x32
    32x32   1:16  --led-rows=32  --led-chain=1
    32x16   1:8   --led-rows=16  --led-chain=2
    16x16   ?     --led-rows=16  --led-chain=1   *
    8x8     1:4   --led-rows=8   --led-chain=1   *(not tested myself)

    * untested.

    Returns:
      List of Lists (matrix) with elements set to None, representing the screen
      shape for the matrix display panels, based on the information above.
    """
    x = y = 0
    if self.matrix_size == 64:
      x = y = self.chain_length
    if self.matrix_size == 32:
      if self.chain_length == 1:
        x = y = self.chain_length
      else:
        x = self.chain_length
        y = 1
    if self.matrix_size == 16:
      x = self.chain_length
      y = 1
    if self.matrix_size == 8:
      x = y = 1
    return [[None for i in range(x)] for i in range(y)]

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
