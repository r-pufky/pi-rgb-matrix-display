#
# Tile Manager for LED RGB Matrix Display.
# 

import time
import matrix_manager
import blank


class TileManager(object):
  """ Manages all tiles and their display on the matrix.
  
  A render pipeline is created, which contains the abstract shape of the matrix
  display screen. Each element in the list is representative of one individual
  matrix tile for displaying.

  A 32 pixel matrix, 2 wide would look like this:

    [[0, 1]]
  
  A square (32x32 matrix) would look like this:

    [[0, 1],
     [0, 1]]

  This pipeline contains indexes to the actual tiles used to generate display
  data for the matrix screen. For these elements there are special meanings:

    -1: A index of -1 represents a 'blank tile'.
    None: A None value represents an 'empty' space.
    +Integer: A positive Integer represents an index into self.tiles.

  A square (32x32 matrix) with a tile, a blank tile and two empty tiles would
  look like this:

    [[3, None],
     [-1, -1]]
  """

  def __init__(self, tiles, led_rows=32, chain_length=2, write_cycles=2,
               tile_size=None, fps=1, static_lifespan=5):
    """ Initalize tile manager.

    Args:
      tiles: List of BaseTile subclassed objects with data to display.
      led_rows: Integer size of RGB matrix hat. Default: 32.
      chain_length: Integer number of matrix's attached. Default: 2.
      write_cycles: Integer write cycle speed, higher is slower. Default: 2.
      tile_size: Integer minimum square tile size in pixels. Default: None (same
        as led_rows).
      fps: Integer max number of frames to render a second, max 60. Default: 1.
          Raspberry Pi's have limited processing power, so 60 is not
          recommended.
      static_lifespan: Integer number of seconds a static tile should be
          displayed before being cleared. Default: 5 seconds.
      render_pipline: List of Lists (matrix) containing Integer indexes
          representing the tile to display. This matrix shape is generated from
          the matrix_manager.
    """
    self.tiles = tiles
    self.matrix = matrix_manager.MatrixInterface(led_rows, chain_length, write_cycles, tile_size)
    self.fps = fps
    self.static_lifespan = static_lifespan
    self.render_pipeline = self.matrix.shape
    (self.max_tile_width, self.max_tile_height) = self._InitalizeTiles()
    if (self.max_tile_width > self.matrix.width or
        self.max_tile_height > self.matrix.height):
      raise Exception('TileManager: A tile cannot be bigger than the screen.')
    self._current_time = 0.0
    self._previous_time = 0.0

  def _InitalizeTiles(self):
    """ Initalizes the default tile state.

    This determines the biggest tile in the set of tiles, as well as set the
    static tile display lifespan for static tiles.

    Returns:
      Tuple (Integer: X, Integer: Y) of max tile size loaded.
    """
    max_screen_width = 0
    max_screen_height = 0
    static_tile_frame_count = self.static_lifespan * self.fps
    for tile in self.tiles:
      (screen_width, screen_height) = tile.GetTileDiemensions()
      max_screen_width = max(screen_width, max_screen_width)
      max_screen_height = max(screen_height, max_screen_height)
      if tile.GetMaxFrames() == 0:
        tile.SetMaxFrameCount(static_tile_frame_count)
    return (max_screen_width, max_screen_height)

  def _GetNextTile(self, size):
    """ Return the next non-displayed tile for the screen.

    This will also mark the tile as 'displayed'.

    Args:
      size: Tuple (Integer: X, Integer: Y) of max tile size needed.

    Returns:
      Integer index of tile that can be rendered next. None if no tile is
      avaliable.
    """
    for index, tile in enumerate(self.tiles):
      if not tile.displayed and tile.GetTileDiemensions() <= size:
        self.tiles[index].displayed = True
        return index
    return None

  def _AllTilesDisplayed(self):
    """ Return Boolean True if all tiles have been displayed.

    All tiles are displayed if the displayed bit is set, and the current frame
    count is >= max frames.
    """
    for tile in self.tiles:
      if not tile.displayed:
        return False
      if not tile.IsExpired():
        return False
    return True

  def _ResetTiles(self):
    """ Resets all tiles to initial non-displayed state. """
    for tile in self.tiles:
      tile.Reset()

  def _RenderPruneAndTick(self):
    """ Check and remove finished tiles from render pipeline, tick frame.
      
    This pipeline contains indexes to the actual tiles used to generate display
    data for the matrix screen. For these elements there are special meanings:

      -1: A index of -1 represents a 'blank tile'.
      None: A None value represents an 'empty' space.
      +Integer: A positive Integer represents an index into self.tiles.
    """
    last_tile_index = None
    for y_index, y_list in enumerate(self.render_pipeline):
      for x_index, tile_index in enumerate(y_list):
        if tile_index is not None:
          if tile_index == -1 or self.tiles[tile_index].IsExpired():
            self.render_pipeline[y_index][x_index] = None
          elif last_tile_index != tile_index:
            last_tile_index = tile_index
            self.tiles[last_tile_index].StepFrame()

  def _RenderAddNewTiles(self):
    """ Add new tiles to render pipeline if space exists.

    If no existing tile will fit, insert a BlankTile to hold the space.
    """

    for y_index, y_list in enumerate(self.render_pipeline):
      for x_index, tile_index in enumerate(y_list):
        if tile_index is None:
          total_empty_tiles = 0
          for i in range(x_index, len(self.render_pipeline[y_index])):
            if self.render_pipeline[y_index][i] is None:
              total_empty_tiles += 1
          new_tile_index = self._GetNextTile(
              (total_empty_tiles * self.matrix.tile_size,
               self.matrix.tile_size))
          if new_tile_index is not None:
            adjust_space = int(self.tiles[new_tile_index].GetTileDiemensions()[0] /
                               self.matrix.tile_size)
            for i in range(x_index, x_index + adjust_space):
              self.render_pipeline[y_index][i] = new_tile_index
          else:
            self.render_pipeline[y_index][x_index] = -1

  def _RenderToMatrix(self):
    """ Compose rendered image and send to matrix for display. """
    y_composite_index = x_composite_index = 0
    last_tile_index = None
    for y_index, y_list in enumerate(self.render_pipeline):
      for x_index, tile_index in enumerate(y_list):
        if tile_index == -1:
          self.matrix.offscreen_buffer.paste(blank.BlankTile().Render(), (x_composite_index, y_composite_index))
        elif last_tile_index != tile_index:
          self.matrix.offscreen_buffer.paste(self.tiles[tile_index].Render(), (x_composite_index, y_composite_index))
          x_composite_index += self.tiles[tile_index].GetTileDiemensions()[0]
          last_tile_index = tile_index
      y_composite_index += self.matrix.tile_size
      x_composite_index = 0
    self.matrix.Render()

  def _RenderSyncFps(self):
    """ Sync rendering to an approximate FPS specified by user. """
    self._current_time = time.time()
    delta = (1.0 / self.fps) - (self._current_time - self._previous_time)
    if delta > 0.0:
      time.sleep(delta)
    self._previous_time = self._current_time

  def Run(self, loop=False):
    """ Run through the displaying of all loaded tiles.

    Args:
      loop: Boolean True to loop infinitely, else loop once. Default: False.
    """
    self.matrix.FillScreen()

    while True:
      self._RenderPruneAndTick()
      self._RenderAddNewTiles()
      self._RenderToMatrix()
      self._RenderSyncFps()

      # If looping indefinitely, reset tiles.
      if self._AllTilesDisplayed():
        if not loop:
          break
        self._ResetTiles()
        self.render_pipeline = self.matrix.shape
