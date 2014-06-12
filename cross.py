import biquad
import bytehelper
import printer

class Biquad:
    name = ""
    coefficients = []
    bytes = []
    def __init__(self, name, coefficients, logger):
        self.name = name
        self.coefficients = coefficients
        bt = bytehelper.ByteHelper()
        logger.log("biquad: %s" % name, printer.LogLevel.Debug)
        logger.printBiquadAsIs(coefficients)
        self.bytes = bt.toBiquadFilterRegister(bt.upshift5(coefficients))
        logger.printBytesAsHex(self.bytes)
    

class CrossoverBand:
    Low = 0
    High = 0
    Biquads = []
    def __init__(self, lo, hi, logger):
        self.Low = lo
        self.High = hi
        self.Biquads = []
        logger.log("band: [%s, %s]" % (lo, hi), printer.LogLevel.Debug)
        

class Crossover:
    bands = []
    bt = bytehelper.ByteHelper()
    logger = printer.Log(printer.LogLevel.All)

    def __init__(self, Fs, Fcs, logger):
        Fcs.insert(0, 0)
        Fcs.append(20000)
        logger.log("Corner freq: %s" % Fcs, printer.LogLevel.Warning)
        for i in range(0, len(Fcs)-1):            
            band = CrossoverBand(Fcs[i], Fcs[i+1], logger)
            if i > 0:
                # hi pass
                bc = biquad.BiquadCalc(Fs, Fcs[i])
                bq = Biquad("HiPass %sHz" % Fcs[i], bc.hipass(), logger)
                band.Biquads.append(bq)
                band.Biquads.append(bq)
            if i < len(Fcs) - 2:
                # low pass
                bc = biquad.BiquadCalc(Fs, Fcs[i+1])
                bq = Biquad("LowPass %sHz" % Fcs[i+1], bc.lowpass(), logger)
                band.Biquads.append(bq)
                band.Biquads.append(bq)
            self.bands.append(band)
            band = None
            
