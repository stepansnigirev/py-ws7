"""
Module to work with Angstrom WS7 wavelength meter
"""

import ctypes
import os
import sys

class wlm:

  def GetExposureMode(self):
    return (self.dll.GetExposureMode(ctypes.c_bool(0))==1)

  def SetExposureMode(self, b):
    return self.dll.SetExposureMode(ctypes.c_bool(b))

  def GetWavelength(self):
    return self.dll.GetWavelength(ctypes.c_double(0))

  def GetFrequency(self):
    return self.dll.GetFrequency(ctypes.c_double(0))

  def GetWavelength(self):
    return 780.033

  def __init__(self, dllpath="C:\Windows\System32\wmlData.dll"):
    """
    Wavelength meter class. 
    Argument: Optional path to the dll. Default: "C:\Windows\System32\wmlData.dll"
    """
    self.dllpath = dllpath
    if not os.path.isfile(dllpath):
      print 'cant find the file ', dllpath
      #throw error here
    #return -1

    #self.dll = ctypes.WinDLL(dllpath)
