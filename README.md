# py-ws7 – minimal wavemeter webserver

py-ws7 is a very simple python webserver that allows to get the wavelength from the High Finesse Angstrom WS7 wavemeter and send it to any computer or phone in your network. Multichannel switch is also supported.

![](extra/screenshot.jpg)

## Features

- Mobile and desktop friendly webserver
- Minimal python module to work with `wlmData.dll` library
- Simple HTTP API to get data (for example with [requests](http://docs.python-requests.org/en/master/))
- Flexible configuration
- Javascript library to embed realtime wavelength value in your pages

## Quick start

Server works on both python2.7 and python3.5. The only dependence is [tornado framework](http://www.tornadoweb.org/en/stable/). You can install it via:

```
pip install tornado
```

To start the server you will need:

- Windows computer with High Finesse software installed and running
- Python 2 or Python 3

Just run in the command line:

```
python server.py
```

Web interface will be available on [http://localhost:8000](http://localhost:8000)

## Configuration

In the project folder there is an example configuration file `config-example.json` where you can see how to set desired channels, labels and custom background. By default server will try to load `config.json` file in the same folder.

## Flags

To find out possible command line arguments run:

```
python server.py -h
```

Flag `--debug` starts the server in debug mode so you can see what it looks like without wavemeter, also on linux or mac computer.

To run server on 80 port (default http port) run:

```
python server.py 80
```

## HTTP API

When server is running you can get wavelengths in json format by simple http requests.

Try adding [/api/](http://localhost:8000/api/) to the url, or [/api/3/](http://localhost:8000/api/3/) to get wavelength of corresponding channel (channels here start from 0).

# Minimal python module `wlm.py`

## `WavelengthMeter` class constructor

WavelengthMeter class accepts two optional arguments:
- `dllpath` - path to the `wlmData.dll`. Default is `C:\Windows\System32\wlmData.dll`
- `debug` - partialy emulates work of the dll library without accessing it, default is `False`

## Class properties

- `wavelengths` - array of all wavelengths (from channel 1 to 8)
- `wavelength` - wavelength of the first channel
- `switcher_mode` - set to True if you want to measure all channels, set to False to measure only active channel

