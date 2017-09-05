#
# Blank Tile for Tile Manager.
#
# This is an empty tile used for filler.
#

from tile_manager import base_tile


class BlankTile(base_tile.BaseTile):
  """ Blank Tile used to fill empty spaces. """

  def __init__(self, x=0, y=0, scrolling=(0,0)):
    """ Initalize blank tile object.

    Args:
      x: Integer absolute X position of tile. Default: 0.
      y: Integer absolute Y position of tile. Default: 0.
      scrolling: Tuple (Integer: X, Integer: Y) containing scrolling
          information. Values are number of pixels to change at once along
          respective axis. Default: (0, 0) (no scrolling).
    """
    base_tile.BaseTile.__init__(self, x, y, scrolling)

  def GetMaxFrames(self):
    """ Returns Integer total number of frames for tile.

    A blank tile only stays for 1 frame, so that it can be immediately replaced
    if another tile has also expired (and a new tile couldn't fit before).

    Returns:
      Integer estimated frames to display all information for tile, or 0 for
      no frames. This is the greater of the X or Y estimates.
    """
    return 1
