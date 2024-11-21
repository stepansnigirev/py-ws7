"""
Module to work with Angstrom WS7 wavelength meter
"""

import ctypes
import random
import sys
import threading
import time

from . import TelnetServer

DLL = None

if sys.platform == "win32":
    DLL_PATH = r"C:\Windows\System32\wlmData.dll"
    try:
        DLL = ctypes.WinDLL(DLL_PATH)
        DLL.GetWavelengthNum.restype = ctypes.c_double
        DLL.GetFrequencyNum.restype = ctypes.c_double
        DLL.GetSwitcherMode.restype = ctypes.c_long
    except OSError:
        print(f"Could not find {DLL_PATH}.")
        print("Using dummy mode.")
        DLL = None


class WavelengthMeter:
    def __init__(
        self, debug=False, poll_time: float = 250e-3, port: int = 1234
    ):
        """Instantiate class.

        Args:
            debug (bool, optional): Debug flag to send dummy data.
                Defaults to False.
            poll_time (float, optional): Polling time of the device in s.
                Defaults to 250e-3.
            port (int, optional): the port on which to set the telnet server.
        """
        self.channels = []
        if DLL is None:
            self.debug = True
        else:
            self.debug = debug
        self.poll_time = poll_time
        self.server = TelnetServer(port=port)
        self.server_running = True
        self.server_thread = threading.Thread(target=self.thread_loop)
        self.server_thread.start()

    def thread_loop(self):
        """Update server loop."""
        while self.server_running:
            self.update_server()
            time.sleep(self.poll_time)

    def update_server(self):
        """Update the server and returns answers to the clients."""
        self.server.update()
        messages = self.server.get_messages()
        for dest, m in messages:
            reply = self.handle_message(m)
            print('reply:',reply)
            self.server.send_message(dest, reply)

    def handle_message(self, message: str) -> str:
        """Handle an incoming client query.

        Args:
            message (str): The message sent by the client.
                This message can either be a "wavelength,i"
                or "frequency,i" message querying the wavelength
                or frequency on channel i.

        Returns:
            str: The corresponding value.
        """
        # Comment this block to test on a local machin without the DLL
        # it will return dummy data
        # if self.debug:
        #     if DLL is None:
        #         error_message = b'DLL not loaded\n\r'
        #         return "DLL not loaded"
        #     return f"You sent: {message}"

        try:
            req, channel = message.split(",")
        except ValueError:
            return "Request not understood ! Should be 'wavelength,i' or 'frequency,i'"
        try:
            channel = int(channel)
        except ValueError:
            return "Channel not understood ! Should be between 1 and 8"
        if req == "wavelength":
            ret = self.get_wavelength(channel)
        elif req == "frequency":
            ret = self.get_frequency(channel)
        else:
            return (
                "Request not understood ! Should be 'wavelength' or 'frequency'"
            )
        return str(ret)

    def get_exposureMode(self) -> bool:
        """Query the exposure mode.

        Returns:
            bool: If the exposure is on.
        """
        if not self.debug:
            return DLL.GetExposureMode(ctypes.c_bool(0)) == 1
        else:
            return True

    def set_exposureMode(self, b: bool) -> int:
        """Turn on or off exposure.

        Args:
            b (bool): True for on, False for off.

        Returns:
            int: 0 for success, 1 else.
        """
        if not self.debug:
            return DLL.SetExposureMode(ctypes.c_bool(int(b)))
        else:
            return 0

    def get_wavelength(self, channel: int = 1) -> float:
        """Get wavelength in nm of specific channel.

        Args:
            channel (int, optional): Channel number. Defaults to 1.

        Returns:
            float: The wavelength in nm.
        """
        if not self.debug:
            return DLL.GetWavelengthNum(
                ctypes.c_long(channel), ctypes.c_double(0)
            )
        else:
            wavelengths = [
                460.8618,
                689.2643,
                679.2888,
                707.2016,
                460.8618 * 2,
                0,
                0,
                0,
            ]
            if channel > 5:
                return 0
            return wavelengths[channel - 1] + channel * random.uniform(
                0, 0.0001
            )

    def get_frequency(self, channel: int = 1) -> float:
        """Get frequency in Thz of specific channel.

        Args:
            channel (int, optional): Channel number. Defaults to 1.

        Returns:
            float: The frequency in THz.
        """
        if not self.debug:
            return DLL.GetFrequencyNum(
                ctypes.c_long(channel), ctypes.c_double(0)
            )
        else:
            return 38434900

    def get_all(self) -> dict:
        """Retrieve all attributes in a dict.

        Returns:
            dict: All available attributes.
        """
        return {
            "debug": self.debug,
            "wavelength": self.GetWavelength(),
            "frequency": self.GetFrequency(),
            "exposureMode": self.GetExposureMode(),
        }

    @property
    def wavelength(self) -> list[float]:
        """Return wavelengths in nm.

        Returns:
            list: A list of wavelengths for each channel.
        """
        return [self.get_wavelength(i + 1) for i in range(8)]

    @property
    def frequency(self) -> list[float]:
        """Return frequencies in THz.

        Returns:
            list: A list of frequencies for each channel.
        """
        return [self.get_frequency(i + 1) for i in range(8)]

    @property
    def switcher_mode(self):
        if not self.debug:
            return DLL.GetSwitcherMode(ctypes.c_long(0))
        else:
            return 0

    @switcher_mode.setter
    def switcher_mode(self, mode):
        if not self.debug:
            DLL.SetSwitcherMode(ctypes.c_long(int(mode)))
        else:
            pass

    def close(self):
        """Close the device."""
        self.server_running = False
        self.server_thread.stop()
        self.server_thread.join()
