#
# Tile Manager for LED RGB Matrix Display.
# 

from tile_manager import matrix_manager


class TileManager(object):
  """ Manages all tiles and their display on the matrix. """
 
  def __init__(self, tiles, matrix_size=32, chain_length=2):
    """ Initalize tile manager.

    Args:
      tiles: List of BaseTile subclassed objects with data to display.
      matrix_size: Integer size of RGB matrix hat. Default: 32.
      chain_length: Integer number of matrix's attached. Default: 2.
    """
    self.matrix = matrix_manager.MatrixInterface(matrix_size, chain_length)
    self.tiles = tiles
    (self.max_tile_width, self.max_tile_height) = self._FindBiggestTile()
    if (self.max_tile_width > self.matrix.screen_width or
        self.max_tile_height > self.matrix.screen_height):
      raise Exception('TileManager: A tile cannot be bigger than the screen.')
    #self.ArrangeTiles()
    #self.tiles_per_screen = self._CalculateTilesPerScreen()
    # LoadTiles -- fits tiles into array for display 

  def ArrangeTiles(self):
    """ Best fit all tiles into given matrix screen.

    See if tiles can be fit together on the matrix either vertically or
    horizontally. Construct a data structure to hold the arrnagement of
    tiles.

    """
    # can we fit multiple per Y row? (all)
    # can we fit multiple per X row? (all)

  def _FindBiggestTile(self):
    """ Determines the biggest tile in the set of tiles.

    Returns:
      Tuple (Integer: X, Integer: Y) of max tile size loaded.
    """
    max_screen_width = 0
    max_screen_height = 0
    for tile in self.tiles:
      (screen_width, screen_height) = tile.GetTileDiemensions()
      max_screen_width = max(screen_width, max_screen_width)
      max_screen_height = max(screen_height, max_screen_height)
    return (max_screen_width, max_screen_height)

  def Run(self, loop=False):
    """ Run through the displaying of all loaded tiles.

    Args:
      loop: Boolean True to loop infinitely, else loop once. Default: False.
    """
    # run loop
    # count secs, execute frame step on FPS count for displayed tiles
    #  check list end. If not looping, exit, otherwise, reset tiles, start at 0
