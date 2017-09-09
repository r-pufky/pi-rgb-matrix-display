#
# Blank Tile unittest.
#

import blank
import unittest


class TestBlankTile(unittest.TestCase):
  """ A blank tile will always have a frame count of 1. """

  def setUp(self):
    """ Initalize BlankTile test setup."""
    self.tile = blank.BlankTile()

  def testStaticFrameCount(self):
    """ Ensure a static tile framecount is generated properly."""
    self.assertEqual(self.tile.GetMaxFrames(), 1)

  def testDynamicFrameCount(self):
    """ Ensure frame counts are generated correctly for moving tiles.

    This implicitly tests _GetFrameCount.
    """
    x_positive_tile = blank.BlankTile(scrolling=(2,0))
    self.assertEqual(x_positive_tile.GetMaxFrames(), 1)
    x_negative_tile = blank.BlankTile(scrolling=(-2,0))
    self.assertEqual(x_negative_tile.GetMaxFrames(), 1)
    y_positive_tile = blank.BlankTile(scrolling=(0,2))
    self.assertEqual(y_positive_tile.GetMaxFrames(), 1)
    y_negative_tile = blank.BlankTile(scrolling=(0,-2))
    self.assertEqual(y_negative_tile.GetMaxFrames(), 1)
    combined_tile = blank.BlankTile(scrolling=(2,2))
    self.assertEqual(combined_tile.GetMaxFrames(), 1)
    combined_negative_tile = blank.BlankTile(scrolling=(-2,-2))
    self.assertEqual(combined_negative_tile.GetMaxFrames(), 1)
    opposing_tile = blank.BlankTile(scrolling=(-1,2))
    self.assertEqual(opposing_tile.GetMaxFrames(), 1)

  def testSetMaxFrameCount(self):
    """ Ensure manually setting the frame count works properly. """
    self.assertEqual(self.tile.GetMaxFrames(), 1)
    self.tile.SetMaxFrameCount(5)
    self.assertEqual(self.tile.GetMaxFrames(), 1)


if __name__ == '__main__':
  unittest.main()