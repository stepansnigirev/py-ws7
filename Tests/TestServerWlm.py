import signal
import sys
import time
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LambdaMeter.WavelengthMeter import WavelengthMeter

# Instantiate the wavemeter
wavemeter = WavelengthMeter(debug=False)
for i, wvl in enumerate(wavemeter.wavelength):
    print(f"Channel {i + 1} - Wavelength: {wvl} nm")
# print("")
for i, freq in enumerate(wavemeter.frequency):
    print(f"Channel {i + 1} - Frequency: {freq} THz")
time.sleep(100)


def signal_handler(sig, frame):
    print("You pressed Ctrl+C!")
    wavemeter.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
while True:
    time.sleep(0.1)
