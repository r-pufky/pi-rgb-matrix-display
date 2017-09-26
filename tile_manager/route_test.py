#
# Mass Transit Route Tile unittest.
#

import datetime
import pytz
import route
import unittest
import unittest_tiletest
from PIL import Image


class TestRouteTile32x32(unittest_tiletest.TileTest):
  """ Ensure primative route tile funcationality works. """

  def setUp(self):
    """ Initalize RouteTile32x32 test setup.

    Statically create a stop time so we know the expected size of text.
    """
    test_time = datetime.datetime(2017, 1, 1,
                                  tzinfo=pytz.timezone('America/Los_Angeles'))
    self.tile = route.RouteTile32x32(stops=[test_time])

  def testInitUtcNowTimezoneAware(self):
    """ Ensure the default utcnow() datetime has no issues with timezones. """
    tile = route.RouteTile32x32()
    self.tile.Render()

  def testGetRenderSize(self):
    """ Ensure the tile can calculate the rendered object size correctly. """
    self.assertEqual(self.tile._GetRenderSize(), (25, 32))

  def testRender(self):
    """ Ensure render works properly. """
    image = self.tile.Render()
    self.assertTrue(self.tile.displayed)
    self.assertIsInstance(image, Image.Image)
    self.AssertSameImage(image, 'testdata/route/test_render.png')


class TestRouteTile32x32Full(unittest_tiletest.TileTest):
  """ Ensure full frame stepping and rendering works. """
  TIMEZONE = pytz.timezone('America/Los_Angeles')

  def setUp(self):
    """ Initalize RouteTile32x32 test setup.

    Statically create a stop time so we know the expected size of text.
    """
    stops = [
        datetime.datetime(2017, 1, 1, 9, 0, tzinfo=self.TIMEZONE),
        datetime.datetime(2017, 10, 11, 10, 0, tzinfo=self.TIMEZONE),
        datetime.datetime(2017, 11, 11, 11, 0, tzinfo=self.TIMEZONE),
        datetime.datetime(2017, 12, 12, 12, 0, tzinfo=self.TIMEZONE)]
    self.tile = route.RouteTile32x32(stops=stops)

  def testStepRender(self):
    """ Test a full run of a sample stop. """
    self.AssertStepRender(self.tile, 'testdata/route/step_render_%02d.png')


if __name__ == '__main__':
  unittest.main()