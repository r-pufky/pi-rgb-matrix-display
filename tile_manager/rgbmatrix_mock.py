#
# Static rbgmatrix python library providing rgbmatrix.so for static mock.
#
# The mock is created to enable testing for non-linux devices or systems which
# do not have the module installed.
#


class Adafruit_RGBmatrix(object):
  """ Mock out the used methods for the matrix. """

  def __init__(self, matrix_size, chain_length):
    self._matrix_size = matrix_size
    self._chain_length = chain_length

  def SetWriteCycles(self, write_cycles):
    self._write_cycles = write_cycles

  def SetImage(self, image, x, y):
    self._image = image
    self._image_x = x
    self._image_y = y

  def Clear(self):
    pass
