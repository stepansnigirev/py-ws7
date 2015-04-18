"""
Module to work with Angstrom WS7 wavelength meter
"""

import ctypes
import os
import sys
import random

class wlm:

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

  def GetWavelength(self):
    if not self.debug:
      return self.dll.GetWavelength(ctypes.c_double(0))/10000.0
    else:
      return round(780.03300+int(random.uniform(0,100))/10000.0,4)

  def GetFrequency(self):
    if not self.debug:
      return self.dll.GetFrequency(ctypes.c_double(0))
    else:
      return 38434900

  def __init__(self, dllpath="C:\Windows\System32\wmlData.dll", debug=False):
    """
    Wavelength meter class. 
    Argument: Optional path to the dll. Default: "C:\Windows\System32\wmlData.dll"
    """
    self.dllpath = dllpath
    if not os.path.isfile(dllpath):
      print 'cant find the file ', dllpath
      #throw error here
    #return -1

    self.debug = debug
    if not debug:
      self.dll = ctypes.WinDLL(dllpath)
