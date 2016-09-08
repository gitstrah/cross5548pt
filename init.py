#!/usr/bin/python
import sys
import cross
from time import sleep
from log import LogLevel
from amp import Amp

amp = Amp()

# mute & init PWM
amp.pwm.mute()
sleep(0.1)
amp.pwm.init()

# I2S input mixer
for channel in amp.PWMs:
	amp.pwm.setInputMixer(channel, amp.I2SMap[channel][0], amp.I2SMap[channel][1])

# Calculate crossover
cr = cross.Crossover(amp.Fs, amp.Fcs, amp.logger)

# Set crossover biquads
# assuming 3-way crossower we must have 3 bands
if len(cr.bands) != 3:
	# too bad!
	amp.logger.log("Expected 3 crossover bands but got %s. Exiting." % (len(cr.bands)), LogLevel.Error)
	sys.exit(-1)

amp.pwm.setBand(amp.Lo_L, cr.bands[0].Biquads)
amp.pwm.setBand(amp.Lo_R, cr.bands[0].Biquads)
amp.pwm.setBand(amp.Mid_L, cr.bands[1].Biquads)
amp.pwm.setBand(amp.Mid_R, cr.bands[1].Biquads)
amp.pwm.setBand(amp.Hi_L, cr.bands[2].Biquads)
amp.pwm.setBand(amp.Hi_R, cr.bands[2].Biquads)

# Set individual chanels volume
for channel in amp.PWMs:
	amp.pwm.setChannelVolume(channel, amp.ChannelVolume[channel])

# Set master volume
amp.pwm.setMasterVolume(amp.volume)

# unmute
#amp.pwm.unmute()

# enjoy