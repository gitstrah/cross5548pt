""" Simple byte operations """
class ByteHelper:
    "TAS5548 PWM modulator helper"
   
    def upshift5(self, coefs):
        return [int(coefs[0]*0x800000), int(coefs[1]*0x800000), 
                int(coefs[2]*0x800000), int(coefs[3]*0x800000),
                int(coefs[4]*0x800000)]     
   
    def split4(self, x):
        a4 = int(x & 0xff)
        a3 = int((x >> 8) & 0xff)
        a2 = int((x >> 16) & 0xff)
        a1 = int(x >> 24) & 0xff 
        return [a1, a2, a3, a4]
