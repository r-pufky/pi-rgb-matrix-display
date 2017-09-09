#
# Weather Tile unittest.
#

import weather
import unittest
import PIL


class TestWeatherTile(unittest.TestCase):

  def setUp(self):
    """ Initalize BaseTile test setup."""
    self.data = {'id': 208,
                 'main': 'sunny',
                 'description': 'sunny and clear.',
                 'icon': '01d',
                 'temp': 72,
                 'temp_min': 68,
                 'temp_max': 78,
                 'humidity': 23}
    self.tile = weather.WeatherTile(self.data)
    self.tile_large = weather.WeatherTile64x32(self.data)

  def testGetRenderSize(self):
    """ Ensure the tile can calculate the rendered object size correctly. """
    self.assertEqual(self.tile._GetRenderSize(), (32, 32))
    self.assertEqual(self.tile_large._GetRenderSize(), (64, 55))

  def testGetRenderSizeLarge(self):
    """ Ensure a large render size is constrained to 64 pixels wide. """
    data = {'id': 208,
            'main': 'sunny',
            'description': 'This is over a 64 pixel long description for the weather tile',
            'icon': '01d',
            'temp': 72,
            'temp_min': 68,
            'temp_max': 78,
            'humidity': 23}
    tile = weather.WeatherTile64x32(data)
    self.assertEqual(tile._GetRenderSize(), (64,55))

  def testRender(self):
    """ Ensure render works properly. """
    image = self.tile_large.Render()
    self.assertTrue(self.tile_large.displayed)
    self.assertIsInstance(image, PIL.Image.Image)


if __name__ == '__main__':
  unittest.main()