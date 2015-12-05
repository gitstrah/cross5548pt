
import printer
import cross
import pwmm
import hardware
from time import sleep
#################################################################################
i2c_addr = 0x1A
log_level = printer.LogLevel.All
#################################################################################

logger = printer.Log(log_level)
i2c = hardware.I2C(i2c_addr, logger)
pwm = pwmm.TAS5548(i2c, logger)

# mute
#pwm.mute()
pwm.unmute()
