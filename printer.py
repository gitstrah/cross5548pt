import bytehelper
from time import gmtime, strftime


class LogLevel():
    All = 1
    Debug = 2
    Warning = 3
    Error = 4

class Log:
    logLevel = LogLevel.Warning;
    def __init__(self, logLevel = LogLevel.Warning):
        self.logLevel = logLevel

    def log(self, s, logLevel = LogLevel.Warning):
        if logLevel >= self.logLevel:            
            print( "%s: %s" % (strftime("%H:%M:%S", gmtime()), s))
    
    def printBiquadAsIs(self, b, logLevel = LogLevel.Debug):        
        self.log("b0 = %s" % b[0], logLevel)
        self.log("b1 = %s" % b[1], logLevel)
        self.log("b2 = %s" % b[2], logLevel)
        self.log("a1 = %s" % b[3], logLevel)
        self.log("a2 = %s" % b[4], logLevel)
        
    def printIntegerBiquadAsHexBytes(self, b, logLevel = LogLevel.Debug):        
        bt = bytehelper.ByteHelper()    
        s = ""
        for x in bt.toBiquadFilterRegister(b):
            s += hex(x) + ' '   
        self.log(s, logLevel)
  
    def bytesToHex(self, b):
        s = ""
        for x in b:
            s += hex(x) + ' ' 
        return s
            
    def printBytesAsHex(self, b, logLevel = LogLevel.Debug):
        self.log(self.bytesToHex(b), logLevel)
  
