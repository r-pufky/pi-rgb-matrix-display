#
# Matrix Manager unittests.
#

import matrix_manager
import unittest


class TestMatrixManager(unittest.TestCase):
  """ Test matrix manager. """

  def setUp(self):
    """ Initalize Matrix Manager test setup. """
    self.matrix = matrix_manager.MatrixInterface()
    self.one = [None]
    self.two = [None, None]

  def testGetMatrixShape64x64(self):
    """ Ensure 64x64 is determined properly. """
    m = matrix_manager.MatrixInterface(led_rows=64,
                                       chain_length=2)
    self.assertEqual(m.shape, [self.one])
    self.assertEqual(m.width, 64)
    self.assertEqual(m.height, 64)
    self.assertEqual(m.tile_size, 64)

  def testGetMatrixShape64x64SmallTile(self):
    """ Ensure 64x64 with small tiles is determined properly. """
    m = matrix_manager.MatrixInterface(led_rows=64,
                                       chain_length=2,
                                       tile_size=32)
    self.assertEqual(m.shape, [self.two, self.two])
    self.assertEqual(m.width, 64)
    self.assertEqual(m.height, 64)
    self.assertEqual(m.tile_size, 32)

  def testGetMatrixShape64x32(self):
    """ Ensure 64x32 is determined properly. """
    m = matrix_manager.MatrixInterface(led_rows=32,
                                       chain_length=2)
    self.assertEqual(m.shape, [self.two])
    self.assertEqual(m.width, 64)
    self.assertEqual(m.height, 32)
    self.assertEqual(m.tile_size, 32)

  def testGetMatrixShape32x32(self):
    """ Ensure 32x32 is determined properly. """
    m = matrix_manager.MatrixInterface(led_rows=32,
                                       chain_length=1)
    self.assertEqual(m.shape, [self.one])
    self.assertEqual(m.width, 32)
    self.assertEqual(m.height, 32)
    self.assertEqual(m.tile_size, 32)

  def testGetMatrixShape32x32SmallTile(self):
    """ Ensure 32x32 is determined properly. """
    m = matrix_manager.MatrixInterface(led_rows=32,
                                       chain_length=1,
                                       tile_size=16)
    self.assertEqual(m.shape, [self.two, self.two])
    self.assertEqual(m.width, 32)
    self.assertEqual(m.height, 32)
    self.assertEqual(m.tile_size, 16)

  def testGetMatrixShape32x16(self):
    """ Ensure 32x16 is determined properly. """
    m = matrix_manager.MatrixInterface(led_rows=16,
                                       chain_length=2)
    self.assertEqual(m.shape, [self.two])
    self.assertEqual(m.width, 32)
    self.assertEqual(m.height, 16)
    self.assertEqual(m.tile_size, 16)

  def testGetMatrixShape16x16(self):
    """ Ensure 16x16 is determined properly. """
    m = matrix_manager.MatrixInterface(led_rows=16,
                                       chain_length=1)
    self.assertEqual(m.shape, [self.one])
    self.assertEqual(m.width, 16)
    self.assertEqual(m.height, 16)
    self.assertEqual(m.tile_size, 16)

  def testGetMatrixShape8x8(self):
    """ Ensure 8x8 is determined properly. """
    m = matrix_manager.MatrixInterface(led_rows=8,
                                       chain_length=1)
    self.assertEqual(m.shape, [self.one])
    self.assertEqual(m.width, 8)
    self.assertEqual(m.height, 8)
    self.assertEqual(m.tile_size, 8)


if __name__ == '__main__':
  unittest.main()
