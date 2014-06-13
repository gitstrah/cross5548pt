
import printer
import cross
import pwmm
import hardware
from time import sleep
#################################################################################
Fs = 96000 # Hz
Fcs = [1800, 5000] # Hz
i2c_addr = 0x1A
log_level = printer.LogLevel.Warning
volume = -40 # dB
#################################################################################

logger = printer.Log(log_level)
i2c = hardware.I2C(i2c_addr, logger)
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
sleep(0.2)

# set all PWM inputs to I2S channel 1
pwm.setInputMixer(1, 1, 0)
pwm.setInputMixer(2, 1, 1)
pwm.setInputMixer(3, 1, 0)
pwm.setInputMixer(4, 1, 1)
pwm.setInputMixer(5, 1, 0)
pwm.setInputMixer(6, 1, 1)

# set crossover biquads
channel = 1
for band in cr.bands:
    setBand(channel, band.Biquads)
    setBand(channel + 1, band.Biquads)
    channel = channel + 2

# set master volume
pwm.setMasterVolume(volume)

# unmute
pwm.unmute()
sleep(0.2)
# enjoy
