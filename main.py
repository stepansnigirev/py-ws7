#!/usr/bin/python

from wlm import wlm

def main():
  meter = wlm("./wlmData-test.dll")
  print 'Current wavelength is', meter.GetWavelength()

if __name__ == "__main__":
  main()
