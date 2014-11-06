#!/usr/bin/env python
import sys
import printer
import hardware
import pwmm
import inspect
from printer import LogLevel

global _BeagleBone        
_BeagleBone = 0
        
# Defaults:
i2c_addr = 0x1A
log_level = printer.LogLevel.All
volume = -40  # dB
isDb = True     # volume is in decibel
logger = printer.Log(LogLevel.All)
        
        
def parseNumber(s):
    s = s.replace("%", "")
    try:
        return float(s)
    except ValueError:
        return float('NaN')

def parseVolume(argVolume):
    isDb = True    
    vol = parseNumber(argVolume)
    if "%" in argVolume:
        isDb = False
    if vol == float('NaN'):
        logger.log("can't parse volume", LogLevel.Error)
    else:
        global volume
        volume = vol        

def parseLogLevel(level):
    return        
        
def parseI2C(address):
    addr = int(address, 16)
    if addr > 0 and addr <=255:
        global i2c_addr
        i2c_addr = addr
        
def printUsage():
    logger.log("usage:\n\tsetvol -v NN%|DD -a ADDR", LogLevel.Warning)
    logger.log("\tNN - volume in percentage from 0 to 100", LogLevel.Warning)
    logger.log("\tDD - volume in decibels value from -128 to 17.5", LogLevel.Warning)
    logger.log("\tADDR - TAS5548 I2C address (hex)", LogLevel.Warning)

if not "-v" in sys.argv:
    printUsage()
    sys.exit()

commands = { "-v": parseVolume,
            "-l": parseLogLevel,
            "-a": parseI2C,
            "-h": printUsage,
             }
# parse arguments
for i in range(len(sys.argv)):
    arg = sys.argv[i] 
    if arg in commands:
        func = commands[arg]
        zz = inspect.getargspec(func)
        if len(inspect.getargspec(func)[0]) == 0:
            commands[arg]
        else:
            commands[arg](sys.argv[i+1])



i2c = hardware.I2C(i2c_addr, logger)
pwm = pwmm.TAS5548(i2c, logger)    
logger.log("setting volume to %s %s" % (volume, ("db" if isDb else "%")), LogLevel.Warning)    
pwm.setMasterVolume(volume)
        


    