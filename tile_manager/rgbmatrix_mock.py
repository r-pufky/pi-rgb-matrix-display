#
# Static rbgmatrix python library providing rgbmatrix.so for static mock.
#
# The mock is created to enable testing for non-linux devices or systems which
# do not have the module installed.
#

import datetime
import os
import pytz


class Adafruit_RGBmatrix(object):
  """ Mock out the used methods for the matrix.

  Attributes:
    LOG_RENDER_BUFFER: Boolean True for SetImage() calls to write image to file.
        Default: False.
    LOG_LOCATION: String location for test render logs to be saved.
    LOG_TIMEZONE: pytz timezone object containing log timezone information.
        Default: America/Los_Angeles.
    last_log_file: String location where last image was logged to.
  """
  LOG_RENDER_BUFFER = False
  LOG_LOCATION = 'testdata/rgbmatrix_mock'
  LOG_TIMEZONE = pytz.timezone('America/Los_Angeles')

  def __init__(self, matrix_size, chain_length):
    self._matrix_size = matrix_size
    self._chain_length = chain_length
    self._log_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        self.LOG_LOCATION)
    if not os.path.isdir(self._log_path) and self.LOG_RENDER_BUFFER:
      raise Exception('Log render buffer specified, but %s log directory does '
                      'not exist!' % self._log_path)      

  def SetWriteCycles(self, write_cycles):
    self._write_cycles = write_cycles

  def SetImage(self, image, x, y):
    self._image = image
    self._image_x = x
    self._image_y = y
    if self.LOG_RENDER_BUFFER:
      now = (datetime.datetime.now(self.LOG_TIMEZONE)
             .astimezone(self.LOG_TIMEZONE)
             .strftime('%Y-%m-%d-%H:%M:%S'))
      log_file = os.path.join(self._log_path, '%s.png' % now)
      self._image.save(log_file)
      self.last_log_file = log_file

  def Clear(self):
    pass
