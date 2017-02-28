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
        request.render("index.html",
            wavelengths=wlmeter.wavelengths,
            **get_config()
        )



static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))
default_config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.json"))

application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/ws/", WsHandler),
], debug=True, static_path=static_path)

# config file parser
class config_action(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        config_file = values
        if not os.path.isfile(config_file):
            raise argparse.ArgumentTypeError("config:{0} is not a valid file".format(config_file))
        if os.access(config_file, os.R_OK):
            setattr(namespace, self.dest, config_file)
        else:
            raise argparse.ArgumentTypeError("config:{0} is not a readable file".format(config_file))

# building configuration
def get_config():
    # command line arguments parsing
    parser = argparse.ArgumentParser(description='Starts a webserver with wavemeter interface.')
    parser.add_argument('--debug', dest='debug', action='store_const',
                        const=True,
                        help='runs the script in debug mode simulating wavelength values')
    parser.add_argument('-c', '--config', action=config_action, default=default_config_file,
                        help='path to config json file, default: config.json in the script folder')
    parser.add_argument('port', type=int, nargs='?',
                        help='server port, default: 8000')

    args = parser.parse_args()

    # default configuration
    config = {
        "port": 8000,
        "precision": 5,
        "debug": False,
        "channels": [{"i": i, "label": "Channel %d" % (i+1)} for i in range(8)]
    }

    # configuration from the file
    with open(args.config, "r") as f:
        config.update(json.loads(f.read()))

    # configuration from command line
    if args.port == None:
        args.port = config["port"]
    config.update(vars(args))

    return config

if __name__ == "__main__":

    config = get_config()

    wlmeter = WavelengthMeter(debug=config["debug"])

    application.listen(config["port"])
    print("Server started at http://localhost:%d" % config["port"])

    PeriodicCallback(send_data, 100).start()

    tornado.ioloop.IOLoop.instance().start()

