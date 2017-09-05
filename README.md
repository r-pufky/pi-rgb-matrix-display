# pi-rgb-matrix-display
Automatically manage and display information on your Raspberry PI &amp; RGB
LED Matrix.

# Installation
This library requires the rgbmatrix.so object to be in your python path. See:
https://github.com/adafruit/rpi-rgb-led-matrix for instructions on compiling.

Using the rgbmatrix.so library requires *root* privileges to access the GPIO
pins.

Additionally, install the follow Python libraries with the follow commands: 

```bash
pip install pytz
pip install Pillow
```

# Usage
```python
import datetime
from tile_manager import tile_manager
from tile_manager import route

tiles = [route.RouteTile('A Line', [datetime.now(), datetime.now()])]
m = tile_manager.TileManager(tiles, 32, 2)
m.Run(loop=True)
```

# Other Files
Both [helvR08.pil](helvR08.pil) and [helvR08.pbm](helvR08.phm) are included in
this repository for ease of use. These are free bitmap fonts from the X11R6
distribution and are not my own work. More information can be found here: 

https://www.x.org/wiki/X11R6/

```
Copyright © 1994 X Consortium.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”, to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE X
CONSORTIUM BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of the X Consortium shall not be
used in advertising or otherwise to promote the sale, use or other dealings in
this Software without prior written authorization from the X Consortium.

X Window System is a trademark of X Consortium, Inc.
```
