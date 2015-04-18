#!/usr/bin/python

from wlm import wlm
import sys

def main():
  debug = False
  args = sys.argv[1:]
  if "-debug" in args:
  	debug = True

  meter = wlm("./wlmData-test.dll", debug)
  print 'Current wavelength is', meter.GetWavelength()

if __name__ == "__main__":
  main()
