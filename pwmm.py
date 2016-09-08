""" TI TAS5548 PWM modulator """
from bytehelper import ByteHelper
from log import LogLevel

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
        self.logger.log("mute", LogLevel.Warning)
        ctrl = self.i2c.readByte(0x03)
        ctrl = ctrl | 0x10
        self.i2c.writeByte(0x03, ctrl)
        pass
        
    def unmute(self):
        # unmute
        self.logger.log("unmute", LogLevel.Warning)
        ctrl = self.i2c.readByte(0x03)
        ctrl = ctrl & ~0x10
        self.i2c.writeByte(0x03, ctrl)
                
    def getVolumeData(self, volume):
        # volume: 0x245 (-128dB) .. 0x001 (17.5dB)
        x = 0x245 - int(0x245*(volume+128)/145.5)
        if x < 1:
            x = 1
        if x > 0x245:
            x = 0x245
        bt = ByteHelper()
        return bt.split4(x)
    
    def setMasterVolume(self, volume):
        "volume[dB]: -128 to 17.5"
        self.logger.log("Master volume = %s dB" % volume, LogLevel.Warning)
        if volume<-128 or volume>17.5:
            self.logger.log("Volume value will be truncated to fit into allowed range: -128 to 17.5 dB", LogLevel.Warning)
        self.i2c.writeList(0xD9, self.getVolumeData(volume))        
    
    def getMasterVolume(self):
        "volume[dB]: -128 to 17.5"
        volume = self.i2c.readWord(0xD9)        
        #x = 0x245 - int(0x245*(volume+128)/145.5)
        x = (0x245-volume) * 145.5 / 0x245 - 128
        self.logger.log("Master volume = %s dB" % x, LogLevel.Warning)
        if x<-128 or x>17.5:
            self.logger.log("Volume does not fit into allowed range: -128 to 17.5 dB", LogLevel.Error)
        return x
    
    def setChannelVolume(self, pwmChannel, volume):
        "volume[dB]: -128 to 17.5"
        # individual channel volume
        self.validatePWMChannel(pwmChannel)
        self.logger.log("Channel %s volume = %s" % (pwmChannel, volume), LogLevel.Warning)
        if volume<-128 or volume>17.5:
            self.logger.log("Volume value will be truncated to fit into allowed range: -128 to 17.5 dB", LogLevel.Warning)
        addresses = [0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8]
        self.i2c.writeList(addresses[pwmChannel-1], self.getVolumeData(volume))

    def setInputMixer(self, pwmChannel, i2sChannel, i2sSubChannel):
        # Input mixers 1, 2, 3, 4, 5, 6, 7, and 8 are mapped into registers 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47,
        # and 0x48, respectively.
        # Each gain coefficient is in 28-bit (5.23) format, so 0x80 0000 is a gain of 1. Each gain coefficient is written
        # as a 32-bit word with the upper four bits reserved. For eight gain coefficients, the total is 32 bytes.
        self.validateI2SChannel(i2sChannel)
        self.validatePWMChannel(pwmChannel)
        self.logger.log("Map PWM %s to I2S %s sub %s" % (pwmChannel, i2sChannel, i2sSubChannel), LogLevel.Warning)        
        addresses = [0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48]
        mix = [0, 0, 0, 0, 0, 0, 0, 0]
        mix[(i2sChannel-1)*2 + i2sSubChannel] = 0x800000        
        self.i2c.writeWords(addresses[pwmChannel-1], mix)
    
    def setBiquadCoefficients(self, pwmChannel, biquadNumber, biquad):
        # set specific biquad
        self.validateBiquadNumber(biquadNumber)
        self.validatePWMChannel(pwmChannel)
        self.logger.log("PWM %s biquad %s - %s" % (pwmChannel, biquadNumber, biquad.name), LogLevel.Warning)
        addresses = [0x51, 0x58, 0x5F, 0x66, 0x6D, 0x74, 0x7B, 0x72]        
        self.i2c.writeWords(addresses[pwmChannel-1] + biquadNumber - 1, biquad.coefficients)         
    
    def setBand(self, pwmChannel, biquads):
        # set specific biquad
        for i in range(0, len(biquads)):
            self.logger.log(biquads[i].name, LogLevel.Debug)
            self.setBiquadCoefficients(pwmChannel, i+1, biquads[i])
        
    def init(self):
        # disable DAP automute
        self.logger.log("disable DAP automute", LogLevel.Warning)
        ctrl = self.i2c.readByte(0x04)
        ctrl = ctrl & ~0x10
        self.i2c.writeByte(0x04, ctrl)
        # --- reset automute control ---
        self.logger.log("reset automute control", LogLevel.Warning)
        # 0x00: Set input automute threshold less than -90dBFS
        # 0x0F: Set input automute and output automute delay to 178.8 ms
        self.i2c.writeByte(0x14, 0x0F)
        # reset PWM automute control
        self.logger.log("reset PWM automute", LogLevel.Warning)
        # 0xF0: Set PWM automute threshold -42dB below input automute threshold
        # 0x07: Set back-end reset period 800 ms
        self.i2c.writeByte(0x15, 0xF7)
        # --- ---
        
    