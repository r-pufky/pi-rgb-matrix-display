#
# Helper unittest library for testing tiles.
#

import math
import operator
import unittest
from PIL import Image
from functools import reduce


import logging


class TileTest(unittest.TestCase):
  """ Added unittest functionality for testing tiles. """

  def AssertSameImage(self, test, filename):
    """ Compares a given image object with 'valid' source image using RMS.

    This determines if there is any difference in the image generated versus
    source of truth, using root mean square. An exact copy will produce a 0.
    Anything less than 5 is ok, as the PIL library generally will save the file
    and the color profile will be lightened slighty.

    Args:
      test: PIL.Image object containing image to test.
      filename: path to image containing source of truth image.

    Asserts:
      Asserts test image is < 5 RMS difference from specified filename image.
    """
    h1 = test.histogram()
    h2 = Image.open(filename).histogram()
    rms = math.sqrt(reduce(operator.add,
                           map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
    self.assertLess(rms, 5)

  def AssertStepRender(self, tile, test_images):
    """ Compares a tile's rendered output with a golden set.

    Args:
      tile: BaseTile or subclass tile object to test.
      test_images: String location with file pattern to compare images. The
          format must include a numeric replacement.

          Example: 'testdata/weather/step_render_large_%02d.png'
    """
    for index in range(tile.GetMaxFrames()):
      self.AssertSameImage(tile.Render(), test_images % index)
      tile.StepFrame()

  def WriteSampleFiles(self, tile, location):
    """ Writes sample images to a specified directory for a given tile.

    Args:
      tile: BastTile or subclass tile object to test.
      location: String location with file pattern to write images. The format
          must include a numeric replacment.

          Example: 'testdata/weather/step_render_large_%02d.png'
    """
    for index in range(tile.GetMaxFrames()):
      logging.error('writing %s', index)
      image = tile.Render()
      image.save(location % index)


if __name__ == '__main__':
  pass
