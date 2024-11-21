# LambdaMeter

## Version 1

This is a minimal fork of [`py-ws7`](https://github.com/stepansnigirev/py-ws7) relying on Telnet for the server / client communication.

This directly implements a server thread running continuously in the Wavemeter class allowing any client to connect and query the
wavelength / frequency as long as one instance is running.

For the Telnet server it relies on [`TelnetServer`](https://github.com/OliverLSanz/python-telnetserver).

## Usage 
### Installation of the server
1. Clone the repository on the computer with the Wavemeter.
2. run `python tests/TestServerWlm.py`

### Installation of the client

1. Clone the repository on the computer with the client.
2. run `python tests/TestClientWlm.py`


## Debug

### Verification of Telnet server client configuration
- run `python examples/SimpleServer.py` to launch the dummy server on the default port 1234.
- In a second terminal run `python examples/SimpleClient.py` to verify the server is running correctly.

### Run some tests ?
- run `python tests/TestServerWlm.py` to launch the server with dummy data (or the real one if you are on the Windows machine and you have the DLL)
- In a second terminal, run `python tests/TestClientWlm.py` to connect to the server and query the wavelength / frequency.
- Update this `print(client.get_wavelength(2))` in the client to get the desired channel.

## Future features ?


- set_exposure from away