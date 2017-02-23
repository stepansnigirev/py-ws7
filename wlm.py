"""
Module to work with Angstrom WS7 wavelength meter
"""

import ctypes, os, sys, random

class WavelengthMeter:

    def __init__(self, dllpath="C:\Windows\System32\wlmData.dll", debug=False):
        """
        Wavelength meter class.
        Argument: Optional path to the dll. Default: "C:\Windows\System32\wlmData.dll"
        """
        self.channels = []
        self.dllpath = dllpath
        self.debug = debug
        if not debug:
            self.dll = ctypes.WinDLL(dllpath)
            self.dll.GetWavelengthNum.restype = ctypes.c_double
            self.dll.GetFrequencyNum.restype = ctypes.c_double

    def GetExposureMode(self):
        if not self.debug:
            return (self.dll.GetExposureMode(ctypes.c_bool(0))==1)
        else:
            return True

    def SetExposureMode(self, b):
        if not self.debug:
            return self.dll.SetExposureMode(ctypes.c_bool(b))
        else:
            return 0

    def GetWavelength(self, channel=1):
        if not self.debug:
            return self.dll.GetWavelengthNum(ctypes.c_long(channel), ctypes.c_double(0))
        else:
            return round(100*channel + 180.03300 + int(random.uniform(0,100)) / 10000.0, 4)

    def GetFrequency(self, channel=1):
        if not self.debug:
            return self.dll.GetFrequencyNum(ctypes.c_long(channel), ctypes.c_double(0))
        else:
            return 38434900

    def GetAll(self):
        return {
            "debug": self.debug,
            "wavelength": self.GetWavelength(),
            "frequency": self.GetFrequency(),
            "exposureMode": self.GetExposureMode()
        }

    @property
    def wavelengths(self):
        return [self.GetWavelength(i) for i in range(1,9)]

    @property
    def wavelength(self):
        return self.GetWavelength(1)

if __name__ == '__main__':
    debug_mode = ('--debug' in sys.argv)
    wlm = WavelengthMeter(debug=debug_mode)
    for i, l in enumerate(wlm.wavelengths):
        print("Wavelength at channel %d:\t%.4f nm" % (i+1, l))

    # print(wlm.channels[0].wavelength)
    # for c in wlm.channels:
    #     print("Channel %d: %.4f nm" % (c.num, c.wavelength))

