#
# Requires the rgbmatrix.so library to exist for test to work.
#

import matrix_manager
import mock
import PIL
import unittest


class TestMatrixManager(unittest.TestCase):
  """
  _GetRenderSize
  Render
  """

  @mock.patch('rgbmatrix.Adafruit_RGBMatrix')
  def setUp(self):
    """ Initalize Matrix Manager test setup. """
    self.matrix = matrix_manager.MatrixInterface()


if __name__ == '__main__':
  unittest.main()