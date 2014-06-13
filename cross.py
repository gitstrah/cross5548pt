""" Crossover class """
from biquad import BiquadCalc
from printer import Log
from printer import LogLevel
from bytehelper import ByteHelper

class Biquad:
    name = ""
    coefficients = []
    def __init__(self, name, coefficients, logger):
        self.name = name        
        bt = ByteHelper()
        logger.log("biquad: %s" % name, LogLevel.Debug, 2)
        logger.printBiquadAsIs(coefficients, LogLevel.Debug, 3)
        self.coefficients = bt.upshift5(coefficients)
        logger.printWordsAsHex(self.coefficients, LogLevel.Debug, 3)
    

class CrossoverBand:
    Low = 0
    High = 0
    Biquads = []
    def __init__(self, lo, hi, logger):
        self.Low = lo
        self.High = hi
        self.Biquads = []
        logger.log("band: [%s, %s]" % (lo, hi), LogLevel.Debug, 1)
        

class Crossover:
    bands = []
    bt = ByteHelper()
    logger = Log(LogLevel.All)

    def __init__(self, Fs, Fcs, logger):
        Fcs.insert(0, 0)
        Fcs.append(20000)
        logger.log("Corner freq: %s" % Fcs, LogLevel.Warning)
        for i in range(0, len(Fcs)-1):            
            band = CrossoverBand(Fcs[i], Fcs[i+1], logger)
            if i > 0:
                # hi pass
                bc = BiquadCalc(Fs, Fcs[i])
                bq = Biquad("HiPass %sHz" % Fcs[i], bc.hipass(), logger)
                band.Biquads.append(bq)
                band.Biquads.append(bq)
            if i < len(Fcs) - 2:
                # low pass
                bc = BiquadCalc(Fs, Fcs[i+1])
                bq = Biquad("LowPass %sHz" % Fcs[i+1], bc.lowpass(), logger)
                band.Biquads.append(bq)
                band.Biquads.append(bq)
            self.bands.append(band)
            band = None
            
