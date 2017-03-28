import argparse
import os, sys

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
from tornado.ioloop import PeriodicCallback
import json

from wlm import WavelengthMeter

# all connected browsers will be here
clients = []

def send_data():
    """Gets wavelengths from the wavemeter and sends it to the client"""
    if len(clients)>0:
        data = wlmeter.wavelengths
        str = json.dumps(data)
        for c in clients:
            c.write_message(str)

class WsHandler(tornado.websocket.WebSocketHandler):
    """Websocket handler"""
    def open(self):
        """Subscribes to the updates by adding itself to the clients list"""
        clients.append(self)

    def on_close(self):
        """Removes itself from clients list"""
        clients.remove(self)
        print('connection closed')

    def check_origin(self, origin):
        """Allows cross origin connection if you want to embed wlm.js library in some page on another domain"""
        return True

class ApiHandler(tornado.web.RequestHandler):
    """Creates simple HTTP API if you don't like websockets"""
    def get(self, channel=None):
        w = wlmeter.wavelengths
        sw = wlmeter.switcher_mode
        if channel is None:
            self.write({ "wavelengths": w, "switcher_mode": sw })
        else:
            ch = int(channel)
            if ch >=0 and ch<len(w):
                self.write("%.8f" % w[ch])
            else:
                self.set_status(400)
                self.write({"error":"Wrong channel"})

class IndexHandler(tornado.web.RequestHandler):
    """Renders index.html page"""
    def get(self):
        self.render("index.html",
            wavelengths=wlmeter.wavelengths,
            **get_config()
        )


default_config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.json"))

def make_app(config):
    """All the routes are defined here"""
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))
    return tornado.web.Application([
            (r"%s/" % config["root"], IndexHandler),
            (r"%s/api/" % config["root"], ApiHandler),
            (r"%s/api/(\d)/" % config["root"], ApiHandler),
            (r"%s/ws/" % config["root"], WsHandler),
            (r"%s/static/(.*)" % config["root"], tornado.web.StaticFileHandler, {'path': static_path}),
    ], debug=True)

class config_action(argparse.Action):
    """Parses config file argument"""
    def __call__(self, parser, namespace, values, option_string=None):
        config_file = values
        if not os.path.isfile(config_file):
            raise argparse.ArgumentTypeError("config:{0} is not a valid file".format(config_file))
        if os.access(config_file, os.R_OK):
            setattr(namespace, self.dest, config_file)
        else:
            raise argparse.ArgumentTypeError("config:{0} is not a readable file".format(config_file))

def get_config():
    """Building configuration dictionary"""

    # command line arguments parsing
    parser = argparse.ArgumentParser(description='Starts a webserver with wavemeter interface.')
    parser.add_argument('--debug', dest='debug', action='store_const',
                        const=True,
                        help='runs the script in debug mode simulating wavelength values')
    parser.add_argument('-c', '--config', action=config_action, default=default_config_file,
                        help='path to config json file, default: config.json in the script folder')
    parser.add_argument('-r', '--root', default=None,
                        help='path where the interface will be, like localhost:8000/root/. Default is "/"')
    parser.add_argument('port', type=int, nargs='?',
                        help='server port, default: 8000')

    args = parser.parse_args()

    # default configuration
    config = {
        "port": 8000, # port
        "root": "/", # path
        "precision": 5, # number of decimals in wavelength display
        "update_rate": 0.1, # how often updates will be sent to the browsers
        "debug": False, # do you want to work with real wavemeter or to test run it?
        "channels": [{"i": i, "label": "Channel %d" % (i+1)} for i in range(8)] # channels to display
    }

    # configuration from the file
    with open(args.config, "r") as f:
        config.update(json.loads(f.read()))

    # configuration from command line
    config["port"] = (args.port or config["port"])
    config["root"] = (args.root or config["root"])
    config["debug"] = (args.debug or config["debug"])

    # add leading slash
    if len(config["root"]) > 0 and config["root"][0] != "/":
        config["root"] = "/"+config["root"]

    # remove trailing slash
    if config["root"][-1] == "/":
        config["root"] = config["root"][:-1]

    return config

if __name__ == "__main__":

    config = get_config()

    wlmeter = WavelengthMeter(debug=config["debug"])

    app = make_app(config)

    if "ssl" in config:
        # https and wss server
        server = tornado.httpserver.HTTPServer(app, xheaders=True, ssl_options=config["ssl"])
    else:
        # http and ws server
        server = tornado.httpserver.HTTPServer(app)

    server.listen(config["port"])
    print("Server started at http://localhost:%d%s/" % (config["port"], config["root"]))

    # periodic callback takes update rate in ms
    PeriodicCallback(send_data, config["update_rate"]*1000).start()

    tornado.ioloop.IOLoop.instance().start()

