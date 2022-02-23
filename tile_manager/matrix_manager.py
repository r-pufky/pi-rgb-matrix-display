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
# Import mangling is used here to support testing for systems without the
# rgbmatrix.so object installed. For all tests to pass, the mock library must be
# used, so the rendering buffer can be verified for accuracy. If tests fails,
# ensure that the rgbmatrix.so library is not installed *OR* manually change
# this import for test verificatin and change it back when deploying.
#

import logging
from PIL import Image
from PIL import ImageDraw

try:
  import rgbmatrix
except ImportError as e:
  logging.error('rgbmatrix.so not found! Loading mock library.')
  # TODO: redo mocks with options object mock as well.
  import rgbmatrix_mock as rgbmatrix


class MatrixInterface(object):
  """ Provides an interface to manipulate the LED Matrix Display.

  ROOT privileges are required to access the GPIO pins.

  Images are drawn in offscreen buffer, then the buffer is moved in place.

  Write Cycles correspond to the refresh rate of the matrix hat, higher is
  slower. This is used to mitigate flickering for displays. General values
  for Raspberry Pi's are: Pi v1: 1, Pi v2/v3: 2.

  Tile Size correspond to the minimum size of a tile used in the matrix
  display. Generally this should be untouched, however in larger display
  matrixes it may make sense to override the default (same as led_rows) and
  create smaller tiles than the specific individual panels (e.g. 128x128
  matrixes).

  For screen shape, the following table is used to automatically generate
  it. If a shape is not implemented but supported, feel free to send a pull
  request to add support to this library.

    https://github.com/hzeller/rpi-rgb-led-matrix

    Type    Scan  Multiplexing   Program Option  Remark
    64x64   1:32  --led-rows=64  --led-chain=2   For displays with E line.
    64x32   1:16  --led-rows=32  --led-chain=2   internally two chained 32x32
    32x32   1:16  --led-rows=32  --led-chain=1
    32x16   1:8   --led-rows=16  --led-chain=2
    8x8     1:4   --led-rows=8   --led-chain=1   *(not tested myself)

    The core library can support up to 32 chained devices, however only the
    above are implemented within this library.

  Attributes:
    led_rows: Integer individual RGB matrix panel size attached. Default: 32.
    chain_length: Integer number of matrix's attached. Default: 2.
    write_cycles: Integer write cycle speed, higher is slower. Default: 2.
    tile_size: Integer minimum square tile size in pixels. Default: None (same
        as led_rows).
    shape: List of Lists (matrix) with elements set to None, representing the
        screen shape for the matrix display panels.
    width: Integer width of the entire matrix screen, in pixels.
    height: Integer height of the entire matrix screen, in pixels.
    offscreen_buffer: Pillow.Image buffer used to prep the next display image.
    offscreen_draw: Pillow.ImageDraw object used to draw shapes onto the
        offscreen_buffer.
  """

  def __init__(self, led_rows=32, chain_length=2,
               write_cycles=2, tile_size=None):
    """ Initialize matrix interface.

    led_rows and chain_length should correspond to --led-rows and
    --led-chain options from demo rgbmatrix code. This is essentially the
    size of your matrix panel and the number of panels that are chained
    together.

    Args:
      led_rows: Integer size of RGB matrix panel attached. Default: 32.
      chain_length: Integer number of matrix's attached. Default: 2.
      write_cycles: Integer write cycle speed, higher is slower. Default: 2.
      tile_size: Integer minimum square tile size in pixels. Default: None (same
          as led_rows).
    """
    self.led_rows = led_rows
    self.chain_length = chain_length
    self.tile_size = tile_size or led_rows
    self._GetMatrixShape()
    self._matrix = rgbmatrix.RGBMatrix(led_rows, chain_length)
    self._matrix.SetWriteCycles(write_cycles)
    self.offscreen_buffer = Image.new('RGB', (self.width, self.height))
    self.offscreen_draw = ImageDraw.Draw(self.offscreen_buffer)
    self.FillScreen()

  def __enter__(self):
    """ Enter runtime context for matrix interface. """
    return self

  def __exit__(self, type, value, traceback):
    """ Exit runtime context for matrix interface, turn screen off. """
    self.TurnOffScreen()

  def _GetMatrixShape(self):
    """ Determines the matrix shape as well as size.

    The shape is determined from the minimum tile size.

    Screen size is returned based on the data from the RGB Matrix library, per:
      https://github.com/hzeller/rpi-rgb-led-matrix. (table above).
    """
    if self.led_rows == 64:
      self.width = self.height = self.led_rows
    if self.led_rows == 32 or self.led_rows == 16:
      self.width = self.led_rows * self.chain_length
      self.height = self.led_rows
    if self.led_rows == 8:
      self.width = self.height = self.led_rows
    
    tiles_x = int(self.width / self.tile_size)
    tiles_y = int(self.height / self.tile_size)
    self.shape = [[None for i in range(tiles_x)] for i in range(tiles_y)]

  def FillScreen(self, fill=(0,0,0)):
    """ Fills the matrix display with a given color.

    Args:
      fill: Tuple containing (Integer: R, Integer: G, Integer: B) values.
          Default: Black (0, 0, 0).
    """
    self.offscreen_draw.rectangle(
        (0, 0, self.width, self.height),
        fill=fill)
    self.Render()

  def Render(self):
    """ Render screen buffer to screen."""
    self._matrix.SetImage(self.offscreen_buffer.im.id, 0, 0)

  def TurnOffScreen(self):
    """ Clears and powers off the screen. """
    if self._matrix:
      self._matrix.Clear()
