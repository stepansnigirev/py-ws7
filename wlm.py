"""
Module to work with Angstrom WS7 wavelength meter
"""

import ctypes
import os
import sys

def GetExposureMode(dll):
  """
  Auto/Manual exposure mode
  Argument: link to the library obtained by wlm.init(path) function
  Returns:  True/False - True if mode is Auto, False otherwise
  """
  return dll.GetExposureMode(ctypes.c_bool(0))

def main():
  """
  This function should be called first to establish connection with wmlData.dll library
  Argument: path to the library
  Returns:  link to the library
  """
  #dllname = 'C:\Windows\System32\wmlData.dll'
  args = sys.argv[1:]
  if not len(args):
    print 'usage: wlm.py path_to_wlmData.dll'
    args[0]='C:\Users\stepansnigirev\AppData\Roaming\Local Libraries\Local Documents\python\py-ws7\wlmData-original.dll'
#    sys.exit(1)
  dllname = args[0]

  print 'loading dll:', dllname
  if not os.path.isfile(dllname):
    print 'cant find the dll, check the path:', dllname
    sys.exit(1)

  dll = ctypes.WinDLL(dllname)
  return dll

if __name__ == "__main__":
  main()
