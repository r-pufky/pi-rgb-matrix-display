#
# TileManager unittest.
#

import blank
import datetime
import math
import operator
import pytz
import route
import tile_manager
import unittest
import weather
from PIL import Image
from functools import reduce


class TestTileManager(unittest.TestCase):
  """ Test basic tile manager functionality. """

  def setUp(self):
    """ Initalize TileManager test setup."""
    self.blank = blank.BlankTile()
    self.route = route.RouteTile()
    self.weather = weather.WeatherTile({})
    self.weather_large = weather.WeatherTile64x32({})
    self.tiles = [self.blank, self.route, self.weather, self.weather_large]
    self.manager = tile_manager.TileManager(self.tiles, 32, 2)

  def testTileLargerThanMatrix(self):
    """ Ensure a tile larger than the matrix screen fails. """
    with self.assertRaises(Exception):
      tile_manager.TileManager([self.blank], 8, 1)

  def testStaticTileFrameCount(self):
    """ Ensure a static tile has appropriate frame count set. """
    static_tile = route.RouteTile(scrolling=(0, 0))
    manager = tile_manager.TileManager([static_tile], 32, 2)
    self.assertEqual(manager.tiles[0].GetMaxFrames(), 5)

  def testGetNextTile(self):
    """ Ensure the correct tile is returned for GetNextTile. """
    self.manager.tiles[0].displayed = True
    tile_index = self.manager._GetNextTile((32, 32))
    self.assertIsInstance(self.manager.tiles[tile_index], route.RouteTile)
    self.assertTrue(self.manager.tiles[tile_index].displayed)

  def testGetNextTileLargeSkipped(self):
    """ Ensure a large tile is skipped properly. """
    tiles = [self.weather_large, self.blank]
    manager = tile_manager.TileManager(tiles, 32, 2)
    tile_index = manager._GetNextTile((32, 32))
    self.assertIsInstance(manager.tiles[tile_index], blank.BlankTile)

  def testAllTilesDisplayed(self):
    """ Ensure all tiles are corrected detected as displayed. """
    self.assertFalse(self.manager._AllTilesDisplayed())
    for tile in self.manager.tiles:
      tile.displayed = True
      tile.current_frame = 100
    self.assertTrue(self.manager._AllTilesDisplayed())

  def testAllTilesDisplayedInvalidCount(self):
    """ Ensure all frames are displayed for all tiles displayed to trigger. """
    for tile in self.manager.tiles:
      tile.displayed = True
    self.assertFalse(self.manager._AllTilesDisplayed())


class TestRenderPipelineTileManager(unittest.TestCase):
  """ Tests related to verifying the rendering pipeline functionality. """

  def setUp(self):
    """ Initalize render pipeline test setup. """
    self.blank = blank.BlankTile()
    self.route = route.RouteTile()
    self.weather = weather.WeatherTile({})
    self.weather_large = weather.WeatherTile64x32({})
    self.tiles = [self.route, self.weather, self.weather_large]
    self.manager = tile_manager.TileManager(self.tiles, 32, 2)

  def AssertCompareImages(self, test, filename):
    """ Compares a given image object with 'valid' source image using RMS.

    This determines if there is any difference in the image generated versus
    source of truth, using root mean square. An exact copy will produce
    a 0. Anything less than 5 is ok, as the PIL library generally will save the
    file and the color profile will be lightened slighty.

    Args:
      test: PIL.Image object containing image to test.
      filename: path to image containing source of truth image.

    Returns:
      Integer value pertaining to 'sameness'. 0 is an exact match.
    """
    h1 = test.histogram()
    h2 = Image.open(filename).histogram()
    rms = math.sqrt(reduce(operator.add,
                           map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
    self.assertLess(rms, 5)

  def testPruneAndTickEmpty(self):
    """ Ensure an empty pipeline works properly. """
    self.manager._RenderPruneAndTick()
    self.assertEqual(self.manager.render_pipeline, [[None, None]])

  def testPruneAndTickTileClear(self):
    """ Ensure an expired tile is removed properly from render pipeline. """
    self.manager.render_pipeline = [[0, 1]]
    self.manager.tiles[1].current_frame = 100
    self.manager._RenderPruneAndTick()
    self.assertIsInstance(
        self.manager.tiles[self.manager.render_pipeline[0][0]],
        route.RouteTile)
    self.assertEqual(
        self.manager.tiles[self.manager.render_pipeline[0][0]].current_frame, 1)
    self.assertIsNone(self.manager.render_pipeline[0][1])

  def testPruneAndTickFull(self):
    """ Ensure a full render pipeline is ticket properly. """
    self.manager.render_pipeline = [[0, 1]]
    self.manager._RenderPruneAndTick()
    self.assertIsInstance(
        self.manager.tiles[self.manager.render_pipeline[0][0]],
        route.RouteTile)
    self.assertEqual(
        self.manager.tiles[self.manager.render_pipeline[0][0]].current_frame, 1)
    self.assertIsInstance(
        self.manager.tiles[self.manager.render_pipeline[0][1]],
        weather.WeatherTile)
    self.assertEqual(
        self.manager.tiles[self.manager.render_pipeline[0][1]].current_frame, 1)

  def testPruneAndTickOneTickBigTile(self):
    """ Ensure a large tile is ticked only once. """
    self.manager.render_pipeline = [[2, 2]]
    self.manager._RenderPruneAndTick()
    self.assertIsInstance(
        self.manager.tiles[self.manager.render_pipeline[0][0]],
        weather.WeatherTile)
    self.assertEqual(
        self.manager.tiles[self.manager.render_pipeline[0][0]].current_frame, 1)
    self.assertIsInstance(
        self.manager.tiles[self.manager.render_pipeline[0][1]],
        weather.WeatherTile)
    self.assertEqual(
        self.manager.tiles[self.manager.render_pipeline[0][1]].current_frame, 1)

  def testAddNewTiles(self):
    """ Ensure adding standard tiles work properly. """
    self.manager._RenderAddNewTiles()
    self.assertEqual(self.manager.render_pipeline, [[0, 1]])

  def testAddNewTilesLargeSkip(self):
    """ Ensure adding a big tile skips the next space properly. """
    self.manager.tiles = [self.weather_large]
    self.manager._RenderAddNewTiles()
    self.assertEqual(self.manager.render_pipeline, [[0, 0]])

  def testAddNewTilesLargeSmallCombined(self):
    """ Ensure adding a large and a small tile on the same row is correct. """
    tiles = [self.weather_large, self.route]
    manager = tile_manager.TileManager(tiles, 32, 4)
    manager._RenderAddNewTiles()
    self.assertEqual(manager.render_pipeline, [[0, 0, 1, -1]])

  def testAddNewTilesLargeNoRoom(self):
    """ Ensure a large tile is not place if there is no room. """
    tiles = [self.route, self.blank, self.weather, self.weather_large]
    manager = tile_manager.TileManager(tiles, 32, 4)
    manager._RenderAddNewTiles()
    self.assertEqual(manager.render_pipeline, [[0, 1, 2, -1]])

  def testAddNewTilesMultiLine(self):
    """ Ensure tile placing works across multiple rows. """
    tiles = [weather.WeatherTile64x32({}),
             weather.WeatherTile64x32({})]
    manager = tile_manager.TileManager(tiles, 64, 4, tile_size=32)
    manager._RenderAddNewTiles()
    self.assertEqual(manager.render_pipeline, [[0, 0],
                                               [1, 1]])

  def testAddNewTilesBlankTiles(self):
    """ Ensure an empty pipeline is filled. """
    tiles = []
    manager = tile_manager.TileManager(tiles, 32, 2)
    manager._RenderAddNewTiles()
    self.assertEqual(manager.render_pipeline, [[-1, -1]])

  def testToMatrix(self):
    """ Ensure a simple render works properly. """
    tiles = [self.route, weather.WeatherTile({'id': 208,
                 'main': 'sunny',
                 'description': 'sunny and clear.',
                 'icon': '01d',
                 'temp': 72,
                 'temp_min': 68,
                 'temp_max': 78,
                 'humidity': 23})]
    manager = tile_manager.TileManager(tiles, 32, 2)
    self.manager._RenderAddNewTiles()
    self.manager._RenderToMatrix()
    self.AssertCompareImages(manager.matrix.offscreen_buffer,
                             'testdata/to_matrix.png')

  def testToMatrixBlankTile(self):
    """ Ensure a blank tile renders properly. """
    tiles = []
    manager = tile_manager.TileManager(tiles, 32, 2)
    manager._RenderAddNewTiles()  
    manager._RenderToMatrix()
    self.AssertCompareImages(manager.matrix.offscreen_buffer,
                             'testdata/to_matrix_blank_tile.png')

  def testToMatrixMultiLine(self):
    """ Ensure a multi line render works properly. """
    tiles = [self.route, self.weather, weather.WeatherTile64x32({'id': 208,
                 'main': 'sunny',
                 'description': 'sunny and clear.',
                 'icon': '01d',
                 'temp': 72,
                 'temp_min': 68,
                 'temp_max': 78,
                 'humidity': 23})]
    manager = tile_manager.TileManager(tiles, 64, 4, tile_size=32)
    manager._RenderAddNewTiles()
    manager._RenderToMatrix()
    self.AssertCompareImages(manager.matrix.offscreen_buffer,
                             'testdata/to_matrix_multiline.png')

class FullTileManagerTest(unittest.TestCase):
  """ Test the tile manager run loop.

  TODO: Implement a Image.save feature in the matrix pipeline to compare
      expected steps through a 'correctly' displayed image.
  """

  def testFullLoop(self):
    weather_large = weather.WeatherTile64x32({'id': 208,
                 'main': 'other',
                 'description': 'sunny and clear.',
                 'icon': '01d',
                 'temp': 72,
                 'temp_min': 68,
                 'temp_max': 78,
                 'humidity': 23}, scrolling=(0,-2))
    stops = [
        datetime.datetime(2017, 1, 1, 9, 0, tzinfo=pytz.timezone('America/Los_Angeles')),
        datetime.datetime(2017, 10, 11, 10, 0, tzinfo=pytz.timezone('America/Los_Angeles')),
        datetime.datetime(2017, 11, 11, 11, 0, tzinfo=pytz.timezone('America/Los_Angeles')),
        datetime.datetime(2017, 12, 12, 12, 0, tzinfo=pytz.timezone('America/Los_Angeles'))]
    tile = route.RouteTile(stops=stops)
    manager = tile_manager.TileManager([weather_large, tile], 32, 2)
    manager.Run()


if __name__ == '__main__':
  unittest.main()
