# py-ws7

A very simple python module to work with High Finesse Angstrom WS 7 wavelength meter.

It can get the wavelength and the frequency from the wavemeter.

Simple example:

```py
wlm = Wavelengthmeter()
for i in range(1,9):
    print("Wavelength at channel %d:\t%.2f" % (i,wlm.GetWavelength(i)))
```
