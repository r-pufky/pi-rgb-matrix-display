#
# Tile Manager for LED RGB Matrix Display.
# 

import time
from tile_manager import matrix_manager


class TileManager(object):
  """ Manages all tiles and their display on the matrix. """
 
  # STATIC PICTURES SHOULD HAVE A MINIMUM CYCLE/DISPLAY TIME.

  def __init__(self, tiles, matrix_size=32, chain_length=2, fps=1):
    """ Initalize tile manager.

    Args:
      tiles: List of BaseTile subclassed objects with data to display.
      matrix_size: Integer size of RGB matrix hat. Default: 32.
      chain_length: Integer number of matrix's attached. Default: 2.
      fps: Integer max number of frames to render a second, max 60. Default: 1.
          Raspberry Pi's have limited processing power, so 60 is not
          recommended.
    """
    self.tiles = tiles
    self.matrix = matrix_manager.MatrixInterface(matrix_size, chain_length)
    self.fps = fps
    self._blank_tile = base_tile.BaseTile()
    (self.max_tile_width, self.max_tile_height) = self._FindBiggestTile()
    if (self.max_tile_width > self.matrix.screen_width or
        self.max_tile_height > self.matrix.screen_height):
      raise Exception('TileManager: A tile cannot be bigger than the screen.')

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

  def _GetNextTile(self, size):
    """ Return the next non-displayed tile for the screen.

    Args:
      size: Tuple (Integer: X, Integer: Y) of max tile size needed.

    Returns:
      Integer index of tile that can be rendered next. None if no tile is
      avaliable.
    """
    for index, tile in enumerate(self.tiles):
      if not tile.displayed and tile.GetTileDiemensions() == size:
        return index

  def _AllTilesDisplayed(self):
    """ Return Boolean True if all tiles have been displayed. """
    for tile in self.tiles:
      if not tile.displayed:
        return False
    return True

  def _ResetTiles(self):
    """ Resets all tiles to initial non-displayed state. """
    for tile in self.tiles:
      tile.Reset()

  def Run(self, loop=False):
    """ Run through the displaying of all loaded tiles.

    Args:
      loop: Boolean True to loop infinitely, else loop once. Default: False.
    """
    screen_space = (self.matrix.screen_width, self.matrix.screen_height)
    render_pipeline = []
    current_time = previous_time = 0.0

    while True:
      # check render pipeline for finished tiles, remove from pipeline, adjust
      render_pipeline = [tile for tile in render_pipeline if tile.current_frame <= tile.GetMaxFrames()]
      for tile in render_pipeline:
        screen_space = tuple(map(operator.add, screen_space, tile.GetTileDiemensions()))

      # Add / updates tiles to render pipeline for display.
      while screen_space > (0,0):
        tile_index = self._GetNextTile(screen_space)
        if tile_index:
          tile = self.tiles[tile_index]
        else:
          tile = self._blank_tile
        tuple(map(operator.sub, screen_space, tile.GetTileDiemensions()))
        render_pipeline.append(tile)

      # Render Tiles (need to compose return images into image for matrix.)
      composite_index = 0
      for tile in render_pipeline:
        self.matrix.offscreen_buffer.paste(tile.Render(), (composite_index, 0))
        composite_index += tile.GetTileDiemensions()[0]
      self.matrix.Render()

      # Hold for approximate FPS
      current_time = time.time()
      delta = (1.0 / self.fps) - (current_time - previous_time)
      if delta > 0.0:
        time.sleep(delta)
      previous_time = current_time

      # If looping indefinitely, reset tiles.
      if self._AllTilesDisplayed():
        if not loop:
          break
        self._ResetTiles()
