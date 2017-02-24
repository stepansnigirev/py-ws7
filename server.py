import argparse
import os, sys

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.ioloop import PeriodicCallback
import json

from wlm import WavelengthMeter

clients = []

def send_data():
    if len(clients)>0:
        data = wlmeter.wavelengths
        for c in clients:
            c.write_message(json.dumps(data))

class WsHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        clients.append(self)

    def on_message(self, message):
        #self.write_message("you wrote: "+message)
        pass

    def on_close(self):
        clients.remove(self)
        print('connection closed')

    def check_origin(self, origin):
        return True

class IndexHandler(tornado.web.RequestHandler):
    def get(request):
        request.render("index.html")

static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))

application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/ws/", WsHandler),
], debug=True, static_path=static_path)

if __name__ == "__main__":

    # command line arguments parsing
    parser = argparse.ArgumentParser(description='Starts a webserver with wavemeter interface.')
    parser.add_argument('--debug', dest='debug', action='store_const',
                        const=True, default=False,
                        help='runs the script in debug mode simulating wavelength values')
    parser.add_argument('port', metavar='port', type=int, nargs='?',
                        help='server port, default: 8000',
                        default=8000)

    args = parser.parse_args()

    wlmeter = WavelengthMeter(debug=args.debug)

    application.listen(args.port)
    print("Server started at http://localhost:%d" % args.port)

    PeriodicCallback(send_data, 100).start()

    tornado.ioloop.IOLoop.instance().start()

