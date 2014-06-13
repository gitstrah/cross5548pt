""" Logging helper """
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

    def log(self, s, logLevel = LogLevel.Warning, tabs = 0):
        if logLevel >= self.logLevel:            
            print( "%s:%s %s" % (strftime("%H:%M:%S", gmtime()), "".ljust(tabs).replace(" ", "  "), s))
    
    def printBiquadAsIs(self, b, logLevel = LogLevel.Debug, tabs = 0):        
        self.log("b0 = %s" % b[0], logLevel, tabs)
        self.log("b1 = %s" % b[1], logLevel, tabs)
        self.log("b2 = %s" % b[2], logLevel, tabs)
        self.log("a1 = %s" % b[3], logLevel, tabs)
        self.log("a2 = %s" % b[4], logLevel, tabs)
        
    def bytesToHex(self, b):
        s = ""
        for x in b:
            s += "{0:0>2X} ".format(x) 
        return s

    def wordsToHex(self, b):
        s = ""
        for x in b:
            s += "{0:0>8X} ".format(x) 
        return s
            
    def printBytesAsHex(self, b, logLevel = LogLevel.Debug, tabs = 0):
        self.log(self.bytesToHex(b), logLevel, tabs)
  
    def printWordsAsHex(self, b, logLevel = LogLevel.Debug, tabs = 0):
        self.log(self.wordsToHex(b), logLevel, tabs)
  
