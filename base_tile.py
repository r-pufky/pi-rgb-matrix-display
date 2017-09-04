#
# Base tile class for managing information displayed on matrix.
#
# This class provides the fundamental abstract class used for all other tiles
# used by TileManager.
#

import math
import operator
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

WHITE = (255, 255, 255)
GRAY = (110, 110, 110)
GREEN = (0, 255, 0)
YELLOW  = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


class BaseTile(object):
  """ Base tile used for all tiles to be displayed on matrix.

  Tiles render using the tile image and redrawing on that image buffer to
  render a frame. To update the 'tile' the image is redrawn with new data
  when the frame is stepped, rendering the new image to the same image
  buffer. More information then the tile size can be displayed using
  scrolling or 'pageflip' techniques on the image buffer.

  A tile is 'finished' when it has stepped through all it's frames. The tile
  may be reset to its initial state any time as well.

  If you want the tile to start rendering 'off' screen and wipe in, then
  you should set the default X/Y values beyond the tile size or below it.
  Otherwise, setting 0/0 will start the tile with the initial data displayed.

  Attributes:
    FONT_Y_OFFSET: Integer Y offset for handling font descenders. Default: -2.
    FONT: ImageFont font to render text in. Default: helvR08.pil.
    TILE_WIDTH: Integer image width. Default: 32 pixels.
    TILE_HEIGHT: Integer image height. Default: 32 pixels.
    x: Integer absolute X position of tile.
    y: Integer absolute Y position of tile.
  """
  FONT_Y_OFFSET = -2
  FONT = ImageFont.load(os.path.dirname(os.path.realpath(__file__)) + '/helvR08.pil')
  TILE_WIDTH = 32
  TILE_HEIGHT = 32

  def __init__(self, x=0, y=0, scrolling=(0,0)):
    """ Initalize base tile.

    Args:
      x: Integer absolute X position tile start in image. Default: 0.
      y: Integer absolute Y position tile start in image. Default: 0.
      scrolling: Tuple (Integer: X, Integer: Y) containing scrolling
          information. Values are number of pixels to change at once along
          respective axis. Default: (0, 0) (no scrolling).
    """
    self.START_X = self.x = x
    self.START_Y = self.y = y
    self.scrolling = scrolling
    self.displayed = False
    self.current_frame = 0
    self._max_frame_count = None
    self._image_buffer = Image.new('RGB', (self.TILE_WIDTH, self.TILE_HEIGHT))
    self._image_draw = ImageDraw.Draw(self._image_buffer)

  def GetTileDiemensions(self):
    """ Returns Tuple (Integer: X, Integer: Y) tile diemensions in pixels.

    This should be the biggest the tile will ever be.
    """
    return (self.TILE_WIDTH, self.TILE_HEIGHT)

  def _GetRenderSize(self):
    """ Determines the total size of the information rendered within a tile.

    Information rendered may be bigger than the tile space allocated, so
    calculate that size. This is used to determine MaxFrames based on
    scrolling speeds.

    Returns:
      Tuple (Integer: X, Integer: Y) size of rendered information.
    """
    return (self.TILE_WIDTH, self.TILE_HEIGHT)

  def GetMaxFrames(self):
    """ Returns Integer total number of frames for tile.

    Tile manager uses this to determine if a tile has shown everything so it
    can be cleared for the next tile.

    Currently, this calculates the number of frames to completely 'wipe' the
    tile. If the tile is static, 0 is returned. The result is cached as this
    should never change for the tile's lifetime.

    Returns:
      Integer estimated frames to display all information for tile, or 0 for
      no frames. This is the greater of the X or Y estimates.
    """
    if self._max_frame_count is None:
      (render_x, render_y) = self._GetRenderSize()
      x_frame_count = self._GetFrameCount(self.scrolling[0], self.START_X, self.TILE_WIDTH, render_x)
      y_frame_count = self._GetFrameCount(self.scrolling[1], self.START_Y, self.TILE_HEIGHT, render_y)
      self._max_frame_count = max(x_frame_count, y_frame_count)
    return self._max_frame_count

  def _GetFrameCount(self, scrolling, start_pos, tile_width, render_width):
    """ Determines the minimum number of frames to shift off screen.

    This is the same for either X or Y translations.

    For positive scrolling:
      - total move = tile width - start position
      - if total move < 0, then it's already off screen.
      - otherwise frame count is ceil(move/|scrolling|)
    For negative scrolling:
      - total move = (start position + objective width) - edge (0 since this
          is always a screen.)
      - if total move < 0, then it's already off screen.
      - otherwise frame count is ceil(move/|scrolling|)

    Args:
      scrolling: Integer scrolling vector.
      start_pos: Integer start position of object.
      tile_width: Integer 'width' of tile.
      render_width: Integer 'width' of object to move.

    Returns:
      Integer maximum number of frames needed to display all information, or
      0 if static image (no frames).
    """
    if scrolling == 0:
      return 0
    if scrolling > 0:
      move = tile_width - start_pos
    else:
      move = start_pos + render_width

    if move < 0:
      return 0
    return math.ceil(move/abs(scrolling))

  def Reset(self):
    """ Reset tile frame state to initial state. """
    self.x = self.START_X
    self.y = self.START_Y
    self.current_frame = 0
    self.displayed = False    

  def StepFrame(self):
    """ Advances tile 1 'frame'.

    This tells the tile to advance the current image 1 'frame', however that
    is interpreted by the subclassed tiles. This is time independent (e.g.
    could be called multiple times before render or not at all).

    Currently, this updates the tile's base X/Y positioning for image rendering
    based on scrolling vector. Alternatively, for more static tiles, this could
    'flip' the image buffer to the next frame in set of images -- if that is
    how you are using it.
    """
    self.current_frame += 1
    (self.x, self.y) = tuple(map(operator.add, self.scrolling, (self.x, self.y)))

  def Render(self):
    """ Returns Image buffer for tile to render.

    Render can be called multiple times, but it is not garanteed that a
    specific time has elapsed; meaning you have would have to determine
    to advance the frame before rendering.

    Once render is called, the tile switches to a 'displayed' state. This has
    no effect on the tile, but enables TileManager to figure out if a tile was
    already displayed.

    By default, a black rectangle is rendered.

    Returns:
      Image containing rendered tile to display.
    """
    self._image_buffer.rectangle((0, 0, self.TILE_WIDTH, self.TILE_HEIGHT),
                                 fill=BLACK)
    self.displayed = True
    return self._image_buffer
