import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LambdaMeter.WavelengthMeterClient import WavelengthMeterClient

## host and port are the default values
client = WavelengthMeterClient(host="10.0.2.103", port=1234)

for i in range(10):
    print(client.get_wavelength(4))
    # print(client.get_exposureMode(2))
    
