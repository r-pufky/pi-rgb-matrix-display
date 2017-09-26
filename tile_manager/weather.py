#
# Weather Tile for Tile Manager.
#

import base_tile
import operator
import os

from PIL import Image


class AbstractWeatherTile(base_tile.BaseTile):
  """ Abstract weather Tile used to handle weather information.

  Attributes:
  """
  ICON_LIBRARY = (os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'openweathermap.org-icons'))

  def __init__(self, weather, x=0, y=0, scrolling=(0,0)):
    """ Initalize weather tile.

    Args:
      weather: Dictionary containing the following weather information:
          {'id': Integer weather type,
           'main': String main weather description,
           'description': String of weather details,
           'icon': String coded icon to use,
           'temp': Integer current temperature,
           'temp_min': Integer minimum temperature,
           'temp_max': Integer maximum temperature,
           'humidity': Integer current humidity}.
      x: Integer absolute X position of tile. Default: 0.
      y: Integer absolute Y position of tile. Default: 0.
      scrolling: Tuple (Integer: X, Integer: Y) containing scrolling
          information. Values are number of pixels to change at once along
          respective axis. Default: (0, 0) (no scrolling).
    """
    base_tile.BaseTile.__init__(self, x, y, scrolling)
    self.weather = weather
    self._icon_cache = None


class WeatherTile32x32(AbstractWeatherTile):
  """ Display a 32x32 wether tile. """

  def _GetRenderSize(self):
    """ Determines the total size of the information rendered within a tile.

    Render the icon on the left, and scroll the text vertically on the right.

    Returns:
      Tuple (Integer: X, Integer: Y) size of rendered information.
    
    Raises:
      Exception if the image icon for the given weather is not found.
   """
    max_height = 0
    for weather_item in self.weather:
      if weather_item not in ['id', 'description', 'icon']:
        max_height += self.FONT.getsize(str(self.weather[weather_item]))[1]

    if not self._icon_cache:
      icon = os.path.join(self.ICON_LIBRARY, '%s.png' % self.weather['icon'])
      if os.path.isfile(icon):
        self._icon_cache = Image.open(icon)
      else:
        raise Exception('WeatherTile: icon file not found: %s' % icon)
    max_height += self._icon_cache.size[1]
    
    return (self.TILE_WIDTH, max_height)

  def Render(self):
    """ Returns Image buffer for tile to render.

    Render can be called multiple times, but it is not garanteed that a
    specific time has elapsed; meaning you have would have to determine
    to advance the frame before rendering.

    Icon | Weather lines

    # Render weather icon and setup for text.
    # Can we optimize by only loading image once and re-writing the right side
    # will artifacts occur? Maybe black rectangle, then re-render text.

    Returns:
      Image containing rendered tile to display.
    
    Raises:
      Exception if the image icon for the given weather is not found.
   """
    self._image_draw.rectangle((0, 0, self.TILE_WIDTH, self.TILE_HEIGHT),
                                fill=base_tile.BLACK)
    if not self._icon_cache:
      icon = os.path.join(self.ICON_LIBRARY, '%s.png' % self.weather['icon'])
      if os.path.isfile(icon):
        self._icon_cache = Image.open(icon)
      else:
        raise Exception('WeatherTile: icon file not found: %s' % icon)

    y = self.y
    self._image_buffer.paste(self._icon_cache, (0, 0))
    y += self._icon_cache.size[1]

    y += self._RenderText(self.x,
                          self.y + self.FONT_Y_OFFSET,
                          self.weather['main'])[1]
    y += self._RenderText(self.x,
                          y + self.FONT_Y_OFFSET,
                          self.weather['temp'])[1]
    y += self._RenderText(self.x,
                          y + self.FONT_Y_OFFSET,
                          'L: %s' % self.weather['temp_min'])[1]
    y += self._RenderText(self.x,
                          y + self.FONT_Y_OFFSET,
                          'H: %s' % self.weather['temp_max'])[1]
    y += self._RenderText(self.x,
                          y + self.FONT_Y_OFFSET,
                          '%%: %s' % self.weather['humidity'])[1]

    self.displayed = True
    return self._image_buffer


class WeatherTile64x32(AbstractWeatherTile):
  """ Display a 64x32 weather tile, one side icon otherside text. """
  TILE_WIDTH = 64

  def _GetRenderSize(self):
    """ Determines the total size of the information rendered within a tile.

    Render the icon on the left, and scroll the text vertically on the right.

    Returns:
      Tuple (Integer: X, Integer: Y) size of rendered information.
    """
    max_height = 0
    for weather_item in self.weather:
      if weather_item not in ['id', 'description', 'icon']:
        max_height += self.FONT.getsize(str(self.weather[weather_item]))[1]
    return (self.TILE_WIDTH, max_height)

  def Render(self):
    """ Returns Image buffer for tile to render.

    Render can be called multiple times, but it is not garanteed that a
    specific time has elapsed; meaning you have would have to determine
    to advance the frame before rendering.

    Icon | Weather lines

    # Render weather icon and setup for text.
    # Can we optimize by only loading image once and re-writing the right side
    # will artifacts occur? Maybe black rectangle, then re-render text.

    Returns:
      Image containing rendered tile to display.

    Raises:
      Exception if the image icon for the given weather is not found.
    """
    self._image_draw.rectangle((0, 0, self.TILE_WIDTH, self.TILE_HEIGHT),
                                fill=base_tile.BLACK)
    if not self._icon_cache:
      icon = os.path.join(self.ICON_LIBRARY, '%s.png' % self.weather['icon'])
      if os.path.isfile(icon):
        self._icon_cache = Image.open(icon)
      else:
        raise Exception('WeatherTile: icon file not found: %s' % icon)

    composite_index = 0
    y = self.y
    self._image_buffer.paste(self._icon_cache, (0, 0))
    composite_index += self._icon_cache.size[0]

    y += self._RenderText(composite_index,
                          self.y + self.FONT_Y_OFFSET,
                          self.weather['main'])[1]
    y += self._RenderText(composite_index,
                          y + self.FONT_Y_OFFSET,
                          self.weather['temp'])[1]
    y += self._RenderText(composite_index,
                          y + self.FONT_Y_OFFSET,
                          'L: %s' % self.weather['temp_min'])[1]
    y += self._RenderText(composite_index,
                          y + self.FONT_Y_OFFSET,
                          'H: %s' % self.weather['temp_max'])[1]
    y += self._RenderText(composite_index,
                          y + self.FONT_Y_OFFSET,
                          '%%: %s' % self.weather['humidity'])[1]

    self.displayed = True
    return self._image_buffer
