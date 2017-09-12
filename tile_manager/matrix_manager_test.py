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

  def setUp(self):
    """ Initalize Matrix Manager test setup. """
    self.matrix = matrix_manager.MatrixInterface()
    self.one = [None]
    self.two = [None, None]
    self.three = [None, None, None]
    self.four = [None, None, None, None]

  def testGetMatrixShape128x128(self):
    """ Ensure 128x128 is determined properly. """
    m = matrix_manager.MatrixInterface(matrix_size=64,
                                       chain_length=4)
    self.assertEqual(m.GetMatrixShape(),
                     [self.four, self.four, self.four, self.four])

  def testGetMatrixShape64x64(self):
    """ Ensure 128x128 is determined properly. """
    m = matrix_manager.MatrixInterface(matrix_size=64,
                                       chain_length=2)
    self.assertEqual(m.GetMatrixShape(),
                     [self.two, self.two])

  def testGetMatrixShape128x32(self):
    """ Ensure 128x128 is determined properly. """
    m = matrix_manager.MatrixInterface(matrix_size=32,
                                       chain_length=4)
    self.assertEqual(m.GetMatrixShape(), [self.four])

  def testGetMatrixShape96x32(self):
    """ Ensure 128x128 is determined properly. """
    m = matrix_manager.MatrixInterface(matrix_size=32,
                                       chain_length=3)
    self.assertEqual(m.GetMatrixShape(), [self.three])

  def testGetMatrixShape64x32(self):
    """ Ensure 128x128 is determined properly. """
    m = matrix_manager.MatrixInterface(matrix_size=32,
                                       chain_length=2)
    self.assertEqual(m.GetMatrixShape(), [self.two])

  def testGetMatrixShape32x32(self):
    """ Ensure 128x128 is determined properly. """
    m = matrix_manager.MatrixInterface(matrix_size=32,
                                       chain_length=1)
    self.assertEqual(m.GetMatrixShape(), [self.one])

  def testGetMatrixShape32x16(self):
    """ Ensure 128x128 is determined properly. """
    m = matrix_manager.MatrixInterface(matrix_size=16,
                                       chain_length=2)
    self.assertEqual(m.GetMatrixShape(), [self.two])

  def testGetMatrixShape16x16(self):
    """ Ensure 128x128 is determined properly. """
    m = matrix_manager.MatrixInterface(matrix_size=16,
                                       chain_length=1)
    self.assertEqual(m.GetMatrixShape(), [self.one])

  def testGetMatrixShape8x8(self):
    """ Ensure 128x128 is determined properly. """
    m = matrix_manager.MatrixInterface(matrix_size=8,
                                       chain_length=1)
    self.assertEqual(m.GetMatrixShape(), [self.one])

if __name__ == '__main__':
  unittest.main()