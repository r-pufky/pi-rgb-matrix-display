#
# Base Tile unittest.
#

import base_tile
import unittest
import PIL


class TestBaseTile(unittest.TestCase):

  def setUp(self):
    """ Initalize BaseTile test setup."""
    self.tile = base_tile.BaseTile()

  def testStaticFrameCount(self):
    """ Ensure a static tile framecount is generated properly."""
    self.assertEqual(self.tile.GetMaxFrames(), 0)

  def testDynamicFrameCount(self):
    """ Ensure frame counts are generated correctly for moving tiles.

    This implicitly tests _GetFrameCount.
    """
    x_positive_tile = base_tile.BaseTile(scrolling=(2,0))
    self.assertEqual(x_positive_tile.GetMaxFrames(), 16)
    x_negative_tile = base_tile.BaseTile(scrolling=(-2,0))
    self.assertEqual(x_negative_tile.GetMaxFrames(), 16)
    y_positive_tile = base_tile.BaseTile(scrolling=(0,2))
    self.assertEqual(y_positive_tile.GetMaxFrames(), 16)
    y_negative_tile = base_tile.BaseTile(scrolling=(0,-2))
    self.assertEqual(y_negative_tile.GetMaxFrames(), 16)
    combined_tile = base_tile.BaseTile(scrolling=(2,2))
    self.assertEqual(combined_tile.GetMaxFrames(), 16)
    combined_negative_tile = base_tile.BaseTile(scrolling=(-2,-2))
    self.assertEqual(combined_negative_tile.GetMaxFrames(), 16)
    opposing_tile = base_tile.BaseTile(scrolling=(-1,2))
    self.assertEqual(opposing_tile.GetMaxFrames(), 32)

  def testGetTileDiemensions(self):
    """ Ensure tile diemensions are generated properly. """
    self.assertEqual(self.tile.GetTileDiemensions(), (32, 32))

  def testSetMaxFrameCount(self):
    """ Ensure manually setting the frame count works properly. """
    self.assertEqual(self.tile.GetMaxFrames(), 0)
    self.tile.SetMaxFrameCount(5)
    self.assertEqual(self.tile.GetMaxFrames(), 5)

  def testStepFrame(self):
    """ Ensure stepping a frame in a tile works properly. """
    self.tile.scrolling = (1, 1)
    self.tile.StepFrame()
    self.assertEqual(self.tile.x, 1)
    self.assertEqual(self.tile.y, 1)
    self.assertEqual(self.tile.current_frame, 1)

  def testReset(self):
    """ Ensure a tile can be reset properly. """
    self.tile.x = 100
    self.tile.y = 50
    self.tile.displayed = True
    self.tile.current_frame = 10
    self.tile.Reset()
    self.assertEqual(self.tile.x, 0)
    self.assertEqual(self.tile.y, 0)
    self.assertFalse(self.tile.displayed)
    self.assertEqual(self.tile.current_frame, 0)

  def testGetRenderSize(self):
    """ Ensure the tile can calculate the rendered object size correctly. """
    self.assertEqual(self.tile._GetRenderSize(), (32, 32))

  def testRenderText(self):
    """ Ensure render text returns the correct rendered size. """
    self.assertEqual(self.tile._RenderText(0, 0, 'hello'), (18, 11))

  def testRenderTextDataConversion(self):
    """ Ensure typecastable data is converted for RenderText. """
    self.assertEqual(self.tile._RenderText(0, 0, 10), (10, 11))
    self.assertEqual(self.tile._RenderText(0, 0, '10'), (10, 11))

  def testRender(self):
    """ Ensure render works properly. """
    image = self.tile.Render()
    self.assertTrue(self.tile.displayed)
    self.assertIsInstance(image, PIL.Image.Image)


if __name__ == '__main__':
  unittest.main()