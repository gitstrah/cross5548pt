'''
Created on Jun 11, 2014

@author: avasilyev
'''
import printer
import bytehelper

class I2C:
    address = 0
    logger = None;
    def __init__(self, address, logger):
        self.address = address
        self.logger = logger
        self.logger.log("I2C created on %s" % hex(address), printer.LogLevel.Debug)
    
    def readByte(self, addr):
        return 0
    
    def writeByte(self, addr, byte):
        self.logger.log("i2c [%s] <= %s" % (hex(addr), hex(byte)))
        pass
    
    def writeList(self, addr, data):
        self.logger.log("i2c [%s] <= %s" % (hex(addr), self.logger.bytesToHex(data)))

class TAS5548:
    i2c = {};
    logger = None
    def __init__(self, i2c, logger):
        self.i2c = i2c
        self.logger = logger
    
    def validatePWMChannel(self, channel):
        pass #TODO: raise exceptions
    
    def validateI2SChannel(self, channel):
        pass #TODO: raise exceptions
    
    def validateBiquadNumber(self, biquadNumber):
        pass #TODO: raise exceptions
    
    def mute(self):
        # mute
        self.logger.log("mute", printer.LogLevel.Warning)
        ctrl = self.i2c.readByte(0x03)
        ctrl = ctrl | 0x10
        self.i2c.writeByte(0x03, ctrl)
        pass
        
    def unmute(self):
        # unmute
        self.logger.log("unmute", printer.LogLevel.Warning)
        ctrl = self.i2c.readByte(0x03)
        ctrl = ctrl & ~0x10
        self.i2c.writeByte(0x03, ctrl)
        pass
        
    def getVolumeData(self, volume):
        # volume: 0x245 (-128dB) .. 0x001 (17.5dB)
        x = 0x245 - int(0x245*(volume+128)/145.5)
        if x < 1:
            x = 1
        if x > 0x245:
            x = 0x245
        bt = bytehelper.ByteHelper()
        return bt.split(x)
    
    def setMasterVolume(self, volume):
        "volume[dB]: -128 to 17.5"
        self.logger.log("Master volume = %s dB" % volume, printer.LogLevel.Warning)
        self.i2c.writeList(0xD9, self.getVolumeData(volume))        
    
    def setChannelVolume(self, pwmChannel, volume):
        # individual channel volume
        self.validatePWMChannel(pwmChannel)
        self.logger.log("channel %s volume = %s" % (pwmChannel, volume), printer.LogLevel.Warning)
        pass        
    
    
    def setInputMapping(self, i2sChannel, pwmChannel1, pwmChannel2):
        # maps input I2S channel to two internal PWM processing channels. 'left'->pwm1, 'right'->'pwm2'
        self.validateI2SChannel(pwmChannel1)
        self.validatePWMChannel(pwmChannel1)
        self.validatePWMChannel(pwmChannel2)
        self.logger.log("Map I2S %s to PWM %s and %s" % (i2sChannel, pwmChannel1, pwmChannel2), printer.LogLevel.Warning)
        # Input mixers 1, 2, 3, 4, 5, 6, 7, and 8 are mapped into registers 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47,
        # and 0x48, respectively.
        # Each gain coefficient is in 28-bit (5.23) format, so 0x80 0000 is a gain of 1. Each gain coefficient is written
        # as a 32-bit word with the upper four bits reserved. For eight gain coefficients, the total is 32 bytes.
        bt = bytehelper.ByteHelper()
        addresses = [0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48]
        mix1 = []
        mix2 = []
        gain0 = 0
        gain1 = 0x800000
        for i in range(1, (i2sChannel-1)*2):
            mix1.append(gain0)
            mix2.append(gain0)
        mix1.append(gain1)
        mix1.append(gain0)
        mix1.append(gain0)
        mix1.append(gain1)
        for i in range(i2sChannel*2+1, 8):
            mix1.append(gain0)
            mix2.append(gain0)
        def flatten(data):
            r = []
            for word in data:
                for b in bt.split(word):
                    r.append(b)
            return r
        self.logger.log("gains for PWM %s: %s" % (pwmChannel1, mix1), printer.LogLevel.Debug)
        self.logger.log("gains for PWM %s: %s" % (pwmChannel2, mix2), printer.LogLevel.Debug)
        self.i2c.writeList(addresses[pwmChannel1], flatten(mix1))
        self.i2c.writeList(addresses[pwmChannel2], flatten(mix2))
        pass        
    
    def setBiquadCoefficients(self, pwmChannel, biquadNumber, biquad):
        # set specific biquad
        self.validateBiquadNumber(biquadNumber)
        self.validatePWMChannel(pwmChannel)
        self.logger.log("PWM %s biquad %s - %s:" % (pwmChannel, biquadNumber, biquad.name), printer.LogLevel.Warning)
        addresses = [0x51, 0x58, 0x5F, 0x66, 0x6D, 0x74, 0x7B, 0x72]        
        self.i2c.writeList(addresses[pwmChannel + biquadNumber - 2], biquad.bytes)         
    
    
    