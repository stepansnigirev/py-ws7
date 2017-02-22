"""
Module to work with Angstrom WS7 wavelength meter
"""

import ctypes
import os
import sys
import random

class Wavelengthmeter:

  def GetAll(self):
    d={}
    d['debug']=self.debug
    d['wavelength']=self.GetWavelength()
    d['frequency']=self.GetFrequency()
    d['exposureMode']=self.GetExposureMode()
    return d

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
      return round(780.03300+int(random.uniform(0,100))/10000.0,4)

  def GetFrequency(self, channel=1):
    if not self.debug:
      return self.dll.GetFrequencyNum(ctypes.c_long(channel), ctypes.c_double(0))
    else:
      return 38434900

  def __init__(self, dllpath="C:\Windows\System32\wlmData.dll", debug=False):
    """
    Wavelength meter class. 
    Argument: Optional path to the dll. Default: "C:\Windows\System32\wlmData.dll"
    """
    self.dllpath = dllpath
    self.debug = debug
    if not os.path.isfile(dllpath):
      print('cant find the file ', dllpath)
      self.debug = True
      #throw error here
    #return -1
    else:
      if not debug:
        self.dll = ctypes.WinDLL(dllpath)
        self.dll.GetWavelengthNum.restype = ctypes.c_double
        self.dll.GetFrequencyNum.restype = ctypes.c_double

if __name__ == '__main__':
  wlm = Wavelengthmeter()
  for i in range(1,9):
    print("Wavelength at channel %d:\t%.2f" % (i,wlm.GetWavelength(i)))
