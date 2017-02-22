import os
import sys

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.ioloop import PeriodicCallback
import json

from wlm import wlm

def logmsg(msg):
  d={}
  d['type']='log'
  d['message']=msg
  return json.dumps(d)

class Sockets(tornado.websocket.WebSocketHandler):
  def open(self):
    if debug:
      mode = 'debug'
    else:
      mode = 'working'
    self.write_message(json.dumps(meter.GetAll()))
    self.callback = PeriodicCallback(self.send_hello, 1000)
    self.callback.start()

  def send_hello(self):
    self.write_message(json.dumps(meter.GetAll()))

  def on_message(self, message):
    #self.write_message("you wrote: "+message)
    pass

  def on_close(self):
    print 'connection closed'

class Server(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  def get(request):
    request.render("index.html")

static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))

application = tornado.web.Application([
    (r"/", Server),
    (r"/websocket", Sockets),
], debug=False, static_path=static_path)

if __name__ == "__main__":
  debug = False
  args = sys.argv[1:]
  if "-debug" in args:
    debug = True

  meter = Wavelengthmeter("./additional/wlmData-test.dll", debug)
  #print 'Current wavelength is', meter.GetWavelength()

  application.listen(8888)
  tornado.ioloop.IOLoop.instance().start()

