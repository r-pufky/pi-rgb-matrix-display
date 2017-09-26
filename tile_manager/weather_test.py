#
# Weather Tile unittest.
#


import unittest
import unittest_tiletest
import weather
from PIL import Image

import logging


class TestWeatherTile(unittest_tiletest.TileTest):

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
    self.tile = weather.WeatherTile32x32(self.data)
    self.tile_large = weather.WeatherTile64x32(self.data)

  def testGetRenderSize(self):
    """ Ensure the tile can calculate the rendered object size correctly. """
    self.assertEqual(self.tile._GetRenderSize(), (32, 87))
    self.assertEqual(self.tile_large._GetRenderSize(), (64, 55))

  def testRender64x32(self):
    """ Ensure render 64x32 works properly. """
    image = self.tile_large.Render()
    self.assertTrue(self.tile_large.displayed)
    self.assertIsInstance(image, Image.Image)
    self.AssertSameImage(image, 'testdata/weather/test_render_large.png')

  def testRender32x32(self):
    """ Ensure render 32x32 works properly. """
    logging.error('writing 32x32 sample files.')
    self.WriteSampleFiles(self.tile, 'testdata/weather/step_render_normal_%02d.png')
    image = self.tile.Render()
    self.assertTrue(self.tile.displayed)
    self.assertIsInstance(image, Image.Image)
    #self.AssertSameImage(image, 'testdata/weather/test_render.png')


class TestWeatherFull(unittest_tiletest.TileTest):
  """ Ensure full frame stepping and rendering works. """

  def setUp(self):
    """ Initalize RouteTile32x32 test setup.

    Statically create a stop time so we know the expected size of text.
    """
    self.data = {'id': 208,
                 'main': 'other',
                 'description': 'sunny and clear.',
                 'icon': '01d',
                 'temp': 72,
                 'temp_min': 68,
                 'temp_max': 78,
                 'humidity': 23}
    self.tile = weather.WeatherTile32x32(self.data, scrolling=(0, -2))
    self.tile_large = weather.WeatherTile64x32(self.data, scrolling=(0, -2))

  def testStepRenderLarge(self):
    """ Test a full run of a sample weather for 64x32 weather tiles. """
    self.AssertStepRender(self.tile_large,
                          'testdata/weather/step_render_large_%02d.png')

  # def testStepRenderNormal(self):
  #   """ Test a full run of a sample weather for 32x32 weather tiles. """
  #   self.AssertStepRender(self.tile,
  #                         'testdata/weather/step_render_normal_%02d.png')


if __name__ == '__main__':
  unittest.main()