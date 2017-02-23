import os
import sys

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

class IndexHandler(tornado.web.RequestHandler):
    def get(request):
        request.render("index.html")

static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))

application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/ws/", WsHandler),
], debug=True, static_path=static_path)

if __name__ == "__main__":
    debug_mode = ('--debug' in sys.argv)

    wlmeter = WavelengthMeter(debug=debug_mode)

    port = 8000
    application.listen(port)
    print("Server started at http://localhost:%d" % port)

    PeriodicCallback(send_data, 100).start()

    tornado.ioloop.IOLoop.instance().start()

