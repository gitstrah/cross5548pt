""" Logging helper """
from time import gmtime, strftime
import os.path


class LogLevel():
    All = 1
    Debug = 2
    Warning = 3
    Error = 4

class Log:
    logLevel = LogLevel.Warning;
    logFile = ""

    def __init__(self, logLevel = LogLevel.Warning, logFile = ""):
        if logFile:
            self.logFile = logFile
        self.logLevel = logLevel        
        path = os.path.dirname(self.logFile)
        if not os.path.isdir(path) and self.logFile:
            try:
                os.makedirs(path)
                print "Created logs folder: %s" % (path)
            except (OSError, IOError):
                print "Unable to create folder %s" % (path)

    def log(self, s, logLevel = LogLevel.Warning, tabs = 0):
        if logLevel >= self.logLevel:    
            message = "%s:%s %s" % (strftime("%H:%M:%S", gmtime()), "".ljust(tabs).replace(" ", "  "), s)
            print(message)
            if self.logFile:
                try:
                    target = open(self.logFile, 'a')
                    target.write(message)
                    target.write('\n')
                    target.close()
                except (OSError, IOError):
                    print "Unable write to %s" % (self.logFile)
    
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

    def tohex(self, val, nbits):
        return hex((val + (1 << nbits)) % (1 << nbits))

    def wordsToHex(self, b):
        s = ""
        for x in b:
            if x < 0:
                s += " %s" % self.tohex(x, 32)
            else:
                s += " {0:0>8X} ".format(x)
        return s.replace("0x", "").upper()
            
    def printBytesAsHex(self, b, logLevel = LogLevel.Debug, tabs = 0):
        self.log(self.bytesToHex(b), logLevel, tabs)
  
    def printWordsAsHex(self, b, logLevel = LogLevel.Debug, tabs = 0):
        self.log(self.wordsToHex(b), logLevel, tabs)
  
