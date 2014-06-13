""" Biquad calculator """
import math

class BiquadCalc:
    "2nd order biquad filter coefficient calculator."
    W = 0; W2 = 0; WQ = 0; N = 0;
    #================================================
    # shared for both lp, hp
    #================================================
    def __init__(self, Fs, Fc, Q = math.sqrt(2)):
        "Fs = sampling frequency, Fc = corner frequency"        
        self.W = math.tan(math.pi * Fc /Fs)
        self.W2 = self.W*self.W
        self.WQ = self.W/Q
        self.N = 1/(self.W2 + self.WQ + 1)
    
    def lowpass(self):
        "Returns [b0, b1, b2, a1, a2]"
        #================================================
        # low-pass H(S) = 1/(S^2 + S/Q + 1)
        #================================================
        b0 = self.N*self.W2
        b1 = 2*b0
        b2 = b0
        a1 = 2*self.N*(self.W2-1)
        a2 = self.N*(self.W2 - self.WQ + 1) 
        return [b0, b1, b2, a1, a2]
    
    def hipass(self):
        "Returns [b0, b1, b2, a1, a2]"
        #================================================
        # high-pass H(S) = S^2/(S^2 + S/Q + 1)
        #================================================
        b0 = self.N
        b1 = -2*self.N
        b2 = b0
        a1 = 2*self.N*(self.W2-1)
        a2 = self.N*(self.W2 - self.WQ + 1)
        return [b0, b1, b2, a1, a2]
    
