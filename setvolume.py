#!/usr/bin/python
import sys
import math
from amp import Amp
from log import LogLevel

amp = Amp()
                
def parseNumber(s):
    s = s.replace("%", "")
    try:
        return float(s)
    except ValueError:
        return float('0') # set volume to 0% if not a number

def printUsage():
    amp.logger.log("usage:\n\tsetvolume.py NN", LogLevel.Error)
    amp.logger.log("\tNN - volume in percent from 0 to 100", LogLevel.Error)

if len(sys.argv) != 2:
    printUsage()
    sys.exit()

volume = parseNumber(sys.argv[1])        

# 100% = 40dB, so convert linear range [1..100] to logarithmic [-128...17.5]
# volume = (128 + 17.5) * 20 * Log10(linearVolume) / (20 * Log10(100)) - 128
# volume = 72.75 * math.log10(volume) - 128
if volume > 0 and volume <= 100:
	logVolume = 72.75 * math.log10(volume) - 128
else:
	logVolume = -128
amp.logger.log("setting volume to %.1f%s or %.2f dB" % (volume, "%", logVolume), LogLevel.Warning)
amp.pwm.setMasterVolume(logVolume)
   