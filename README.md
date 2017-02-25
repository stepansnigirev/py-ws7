# Minimal High Finesse Angstrom WS7 wavemeter python module and webserver

A set of python scripts to make work with High Finesse Angstrom WS 7 wavelength meter more convinient. Multichannel switching also works.

Unfortunately it works only on windows and requires a running original application. To make it available in your network via web browser run `server.py`.

Tested to work in Python 3.5 and Python 2.7.

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
python3 server.py
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

## `WavelengthMeter` class constructor

WavelengthMeter class accepts two optional arguments:
- `dllpath` - path to the `wlmData.dll`. Default is `C:\Windows\System32\wlmData.dll`
- `debug` - partialy emulates work of the dll library without accessing it, default is `False`

## Class methods

- `wavelengths` - array of all wavelengths (from channel 1 to 8)
- `wavelength` - wavelength of the first channel
- `switcher_mode` - set to True if you want to measure all channels, set to False to measure only active channel

# Web interface

## Configuration

## HTTP API

