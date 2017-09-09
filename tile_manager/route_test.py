#
# Mass Transit Route Tile unittest.
#

import datetime
import PIL
import pytz
import route
import unittest


class TestRouteTile(unittest.TestCase):

  def setUp(self):
    """ Initalize RouteTile test setup.

    Statically create a stop time so we know the expected size of text.
    """
    test_time = datetime.datetime(2017, 1, 1,
                                  tzinfo=pytz.timezone('America/Los_Angeles'))
    self.tile = route.RouteTile(stops=[test_time])

  def testInitUtcNowTimezoneAware(self):
    """ Ensure the default utcnow() datetime causes no issues with timezones. """
    tile = route.RouteTile()
    self.tile.Render()

  def testGetRenderSize(self):
    """ Ensure the tile can calculate the rendered object size correctly. """
    self.assertEqual(self.tile._GetRenderSize(), (26, 11))

  def testRender(self):
    """ Ensure render works properly. """
    image = self.tile.Render()
    self.assertTrue(self.tile.displayed)
    self.assertIsInstance(image, PIL.Image.Image)


if __name__ == '__main__':
  unittest.main()