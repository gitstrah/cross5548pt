""" Hardware abstraction """
from time import sleep
from Adafruit_I2C import Adafruit_I2C
    
from bytehelper import ByteHelper
from log import LogLevel

class I2C:
    """I2C hardware abstraction"""
    address = 0
    i2c = None
    logger = None
    bt = ByteHelper()
    def __init__(self, address, logger, beagleBone):
        self.address = address
        self.logger = logger
        self.logger.log("I2C created on %s" % hex(address), LogLevel.Debug)   
        self.beagleBone = beagleBone
        if beagleBone:
            self.i2c = Adafruit_I2C(self.address)     
    
    def readByte(self, addr):
        if self.beagleBone:
            return self.i2c.readU8(addr)
        return 0
    
    def readWord(self, addr):
        b = [0,0,0,0]
        bt = ByteHelper()
        if self.beagleBone:
            b = self.i2c.readList(addr, 4)
            self.logger.log("verify: %s" % self.logger.bytesToHex(b), LogLevel.Debug, 2)
        word = bt.join4(b)
        self.logger.log("word: %s" % self.logger.wordsToHex([word]), LogLevel.Debug, 2)
        return word

    def writeByte(self, addr, byte):
        self.logger.log("i2c [{0:0>2X}] <= {1:0>2X}".format(addr, byte), LogLevel.Debug, 1)
        if self.beagleBone:
            self.i2c.write8(addr, byte)
    
    def writeList(self, addr, data):
        # write operations to be broken up into multiple data write operations that are multiples of four data bytes        
        a = addr
        for i in range(0, len(data)/4):
            b = []
            if i > 0:
                a = 0xFE
            for j in range(0, 4):
                b.append(data[(i)*4 + j])
            self.logger.log("i2c [{0:0>2X}] <= {1}".format(a, self.logger.bytesToHex(b)), LogLevel.Debug, 1)
            
            if self.beagleBone:
                self.i2c.writeList(a, b)
                #sleep(0.2)
        if self.beagleBone:
            b = self.i2c.readList(addr, len(data))
            #self.logger.log("    verify: %s" % b)
            self.logger.log("verify: %s" % self.logger.bytesToHex(b), LogLevel.Debug, 2)
            
    def writeWords(self, addr, data):
        b = []
        for word in data:
            for x in self.bt.split4(word):
                b.append(x)
        self.writeList(addr, b)
            
        
            