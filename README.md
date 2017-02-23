# py-ws7

A set of python scripts to make work with High Finesse Angstrom WS 7 wavelength meter more convinient. Multichannel extension is also supported.

Unfortunately it works only on windows and requires a running original application. To make it available in your network via http requests run `webserver.py`.

Tested to work in python3.5.

# This project is in development!

Documentation is not complete yet. Better look at the code itself.

# Quick start

## Simple example

```py
from wlm import WavelengthMeter

wlm = WavelengthMeter()
for i, l in enumerate(wlm.wavelengths):
    print("Wavelength at channel %d:\t%.4f nm" % (i+1, l))
```

This example will print wavelengths of every channel of the wavemeter.

## Web interface

You can also run a webserver to make your wavemeter available over the network. It includes a web interface and http API.

Simply run a webserver script:

```
python3 webserver.py 8000
```

Now you can open [http://localhost:8000/](http://localhost:8000/) in your browser to see the web interface.

All the information about the webserver's API is available from the menu of the web interface (/help/) or [here](#web-interface-1).

# Installation

To get data from the wavemeter you will need:
- A wavemeter itself connected to the computer
- Windows
- Original High Finesse software running

For testing and debugging without access to the wavemeter and software you can use a [dummy library](wlmData/wlmData-test.dll). But still you need Windows.

A core module `wlm.py` doesn't have any python dependencies.

Webserver script requires tornado. So if you want to run a webserver, install it:

```
pip install tornado
```

# Core module `wlm.py`

# Web interface

## Configuration

## HTTP API

# TODO

- `python3 wlm.py --debug`
- `python3 wlm -p [--path] "C:\blahblahblah"`
- wavelength and wavelengths @properties
- Normal server and a page
- Mobile and desktop