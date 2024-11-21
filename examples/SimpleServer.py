import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LambdaMeter.TelnetServer import TelnetServer as TelnetServer

class WvlServer(TelnetServer):
    def __init__(self, port=1234):
        super().__init__(encoding="utf-8", error_policy='replace', port=port)

if __name__ == "__main__":
    import time
    server = WvlServer()
    while True:
        server.update()
        msg = server.get_messages()
        print(f'msg: {msg}')
        for dest, m in msg:
            server.send_message(dest, f"You sent: {m}")
        time.sleep(1)