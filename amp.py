
from log import LogLevel
from log import Log
import pwmm
import hardware


class Amp:
	#################################################################################
	# Settings Mappigs.
	#################################################################################
	# TAS 5548 PWM channel mapping
	Lo_L	= 1
	Lo_R	= 2
	Mid_L	= 3
	Mid_R	= 4
	Hi_L	= 5
	Hi_R	= 6
	PWMs = [Lo_L, Lo_R, Mid_L, Mid_R, Hi_L, Hi_R]
	#PWMs = [Lo_L, Lo_R]

	# I2S input mapping as [I2S channel , subchannel: 0=R 1=L]
	I2SMap = {}
	I2SMap [Lo_L] = [1, 1]
	I2SMap [Lo_R] = [1, 0]
	I2SMap [Mid_L] = [1, 1]
	I2SMap [Mid_R] = [1, 0]
	I2SMap [Hi_L] = [1, 1]
	I2SMap [Hi_R] = [1, 0]

	# individual channel volume adjustment in dB
	ChannelVolume = {}
	ChannelVolume[Lo_L] = 0
	ChannelVolume[Lo_R] = 0
	ChannelVolume[Mid_L] = -7
	ChannelVolume[Mid_R] = -7
	ChannelVolume[Hi_L] = -6
	ChannelVolume[Hi_R] = -6

	Fs = 96000 # Hz
	Fcs = [1000, 6500] # Hz
	i2c_addr = 0x1A
	log_level = LogLevel.Warning
	#log_level = LogLevel.Debug
	volume = -15 # dB	
	_BeagleBone = 1
	def __init__(self):
		self.logger = Log(self.log_level, "logs/hw.log")
		self.i2c = hardware.I2C(self.i2c_addr, self.logger, self._BeagleBone)
		self.pwm = pwmm.TAS5548(self.i2c, self.logger)
