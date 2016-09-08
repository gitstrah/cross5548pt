#!/usr/bin/python
import sys
import math
from amp import Amp

amp = Amp()

# logVolume = 72.75 * math.log10(volume) - 128
# so linearVolume = (logVolume + 128) / 72.5 
volume = amp.pwm.getMasterVolume()
if volume < -128 or volume > 17.5:
	volume = -128
linearVolume = math.ceil(math.pow(10, (volume + 127) / 72.25))
if linearVolume < 1:
	linearVolume = 0
if linearVolume > 100:
	linearVolume = 100
print "%d" % (linearVolume)

