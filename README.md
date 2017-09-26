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

# Testing
Standard Python unit testing framework tests apply.

```bash
cd pi-rgb-matrix-display/tile_manager
python -m unittest discover -p '*_test.py'
```

# Other Files

## helvR08.pil & helvR08.pbm
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

## openweathermap.org icons (resized)
[openweathermap.org icons](tile_manager/openweathermap.org-icons/README.md) fall
under their terms of service for creative common usage. Licensing info also
listed within that directory:

Icons included in this directory were resized from 50x50 to 32x32 to fit the RGB
Matrix screen. This is *NOT* my original work, all artwork belongs to
openweathermap.org, under the creative commons v4.0 license.

Original Icons are found here:
* http://openweathermap.org/weather-conditions

Original Icons can be accessed via URL here:
* http://openweathermap.org/img/w/*.png

Create Commons v4.0 License https://creativecommons.org/licenses/by-sa/4.0/

This is included in this directory as [LICENSE](LICENSE)


[Terms of Service](http://openweathermap.org/terms)
```
Please read these terms of use carefully before you start to use the
OpenWeatherMap.org site. By using our site, you indicate that you accept these
terms of use and that you agree to abide by them. If you do not agree to these
terms of use, please refrain from using our site.

Reliance on information posted & Disclaimer The materials contained on our site
are provided for general information purposes only and do not claim to be or
constitute legal or other professional advice and shall not be relied upon as
such.

We do not accept any responsibility for any loss which may arise from accessing
or reliance on the information on this site and to the fullest extent permitted
by English law, we exclude all liability for loss or damages direct or indirect
arising from use of this site.

Information about us OpenWeatherMap Inc.  1979 Marcus Avenue  Suite 210  Lake
Success, NY  11042

OpenWeatherMap SIA  Registration number 40103961603  Matīsa iela 79, Rīga,
LV-1009  Latvia  VAT LV40103961603 You can contact us by writing to the business
address given above or via Support Center.

Accessing our site Access to our site is permitted on a temporary basis, and we
reserve the right to withdraw or amend the service we provide on our site
without notice (see below). We will not be liable if for any reason our site is
unavailable at any time or for any period.

Copyright We are the owner or the licensee of all intellectual property rights
in our site, and in the material published on it. Those works are protected by
copyright laws and treaties around the world. All such rights are reserved.

You may print off one copy, and may download extracts, of any page(s) from our
site for your personal reference and you may draw the attention of others within
your organisation to material posted on our site.

You must not modify the paper or digital copies of any materials you have
printed off or downloaded in any way, and you must not use any illustrations,
photographs, video or audio sequences or any graphics separately from any
accompanying text.

Our status (and that of any identified contributors) as the authors of material
on our site must always be acknowledged.

You must not use any part of the materials on our site for commercial purposes
without obtaining a licence to do so from us or our licensors.

If you print off, copy or download any part of our site in breach of these terms
of use, your right to use our site will cease immediately and you must, at our
option, return or destroy any copies of the materials you have made.

Licenses Free weather API is provided under the terms of the Creative Commons
Attribution-ShareAlike 4.0 Generic License.

Any use of the work other than as authorized under this license or copyright law
is prohibited.

You are free to:

Share — copy and redistribute the material in any medium or format

Adapt — remix, transform, and build upon the material

for any purpose, even commercially.

The licensor cannot revoke these freedoms as long as you follow the license
terms.

Under the following terms:

Attribution — You must give appropriate credit, provide a link to the
OpenWeatherMap.org, and indicate if changes were made. You may do so in any
reasonable manner, but not in any way that suggests the licensor endorses you or
your use.

ShareAlike — If you remix, transform, or build upon the material, you must
distribute your contributions under the same license as the original.

No additional restrictions — You may not apply legal terms or technological
measures that legally restrict others from doing anything the license permits.

You do not have to comply with the license for elements of the material in the
public domain or where your use is permitted by an applicable exception or
limitation.

No warranties are given. The license may not give you all of the permissions
necessary for your intended use. For example, other rights such as publicity,
privacy, or moral rights may limit how you use the material.

Other licenses different from Creative Commons can be used in Elite accounts
under conditions set out in the price-list.

Payment You agree to pay the full price for the service you purchase from the
Website under conditions set out in the price-list. We reserve the right to
charge extra charges for your credit card or PayPal account for any products
purchased from the Website. You are responsible for the timely payment of all
fees and for providing us with a valid credit card or PayPal account details for
payment of all fees. No refunds will be given after monthly or longer period
fees have been made.

Our site changes regularly We aim to update our site regularly, and may change
the content at any time. If the need arises, we may suspend access to our site,
or close it indefinitely. Any of the material on our site may be out of date at
any given time, and we are under no obligation to update such material.

Our liability The material displayed on our site is provided without any
guarantees, conditions or warranties as to its accuracy. To the extent permitted
by law, we, and third parties connected to us hereby expressly exclude:

All conditions, warranties and other terms which might otherwise be implied by
statute, common law or the law of equity. Any liability for any direct, indirect
or consequential loss or damage incurred by any user in connection with our site
or in connection with the use, inability to use, or results of the use of our
site, any websites linked to it and any materials posted on it, including,
without limitation any liability for: loss of income or revenue; loss of
business; loss of profits or contracts; loss of anticipated savings; loss of
data; loss of goodwill; wasted management or office time; and for any other loss
or damage of any kind, however arising and whether caused by tort (including
negligence), breach of contract or otherwise, even if foreseeable, provided that
this condition shall not prevent claims for loss of or damage to your tangible
property or any other claims for direct financial loss that are not excluded by
any of the categories set out above.

This does not affect our liability for death or personal injury arising from our
negligence, nor our liability for fraudulent misrepresentation or
misrepresentation as to a fundamental matter, nor any other liability which
cannot be excluded or limited under applicable law.

Information about you and your visits to our site We process information about
you in accordance with our privacy policy.

By using our site, you consent to such processing and you warrant that all data
provided by you is accurate.

Viruses, hacking and other offences You must not misuse our site by knowingly
introducing viruses, trojans, worms, logic bombs or other material which is
malicious or technologically harmful. You must not attempt to gain unauthorised
access to our site, the server on which our site is stored or any server,
computer or database connected to our site. You must not attack our site via a
denial-of-service attack or a distributed denial-of service attack.

By breaching this provision, you would commit a criminal offence under the
Computer Misuse Act 1990. We will report any such breach to the relevant law
enforcement authorities and we will co-operate with those authorities by
disclosing your identity to them. In the event of such a breach, your right to
use our site will cease immediately.

We will not be liable for any loss or damage caused by a distributed denial-of-
service attack, viruses or other technologically harmful material that may
infect your computer equipment, computer programs, data or other proprietary
material due to your use of our site or to your downloading of any material
posted on it, or on any website linked to it.

Links from our site Where our site contains links to other sites and resources
provided by third parties, these links are provided for your information only.
We have no control over the contents of those sites or resources, and accept no
responsibility for them or for any loss or damage that may arise from your use
of them. When accessing a site via our website we advise you check their terms
of use and privacy policies to ensure compliance and determine how they may use
your information.

Variations We may revise these terms of use at any time by amending this page.
You are expected to check this page from time to time to take notice of any
changes we made, as they are binding on you. Some of the provisions contained in
these terms of use may also be superseded by provisions or notices published
elsewhere on our site.

Your concerns If you have any concerns about material which appears on our site,
please contact us.

Thank you for visiting our site.
```
