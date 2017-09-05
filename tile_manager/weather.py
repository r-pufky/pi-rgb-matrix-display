#
# Weather Tile for Tile Manager.
#

from tile_manager import base_tile
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class WeatherTile(base_tile.BaseTile):
  """ Tile used to handle weather information.

  Attributes:
  """

  def __init__(self, x=0, y=0, scrolling=(0,0)):
    """ Initalize weather tile.

    Args:
      x: Integer absolute X position of tile. Default: 0.
      y: Integer absolute Y position of tile. Default: 0.
      scrolling: Tuple (Integer: X, Integer: Y) containing scrolling
          information. Values are number of pixels to change at once along
          respective axis. Default: (0, 0) (no scrolling).
    """
    base_tile.BaseTile.__init__(self, x, y, scrolling)
