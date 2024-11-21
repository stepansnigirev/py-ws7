from telnetlib import Telnet
import time

client = Telnet(host='localhost', port=1234)
for i in range(100):
    client.write("Hello".encode())
    time.sleep(1)
    print(client.read_until("\n\r".encode()).decode())
client.close()