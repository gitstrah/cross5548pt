import printer
import cross
import pwmm
from time import sleep
#################################################################################
Fs = 96000
Fcs = [1800, 5000]
i2c_addr = 0
log_level = printer.LogLevel.All
volume = -40
#################################################################################

logger = printer.Log(log_level)
i2c = pwmm.I2C(i2c_addr, logger)
pwm = pwmm.TAS5548(i2c, logger)

def setBand(pwmChannel, biquads):
        # set specific biquad
        for i in range(0, len(biquads)):
            logger.log(biquads[i].name, printer.LogLevel.Debug)
            pwm.setBiquadCoefficients(pwmChannel, i+1, biquads[i])
        pass
# crossover
cr = cross.Crossover(Fs, Fcs, logger)
# mute
pwm.mute()
sleep(1)
# set inputs
pwm.setInputMapping(1, 1, 2)
pwm.setInputMapping(1, 3, 4)
pwm.setInputMapping(1, 5, 6)
# set crossover biquads
# pwm.setBiquadCoefficients(pwmChannel, biquadNumber, cr.bands[0].Biquads)

channel = 1
for band in cr.bands:
    setBand(channel, band.Biquads)
    setBand(channel + 1, band.Biquads)
    channel = channel + 2
# set volume
pwm.setMasterVolume(volume)
# unmute
pwm.unmute()
sleep(0.2)
# enjoy
