import os, uuid

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler

from lib import MouseEvent

rel = lambda *x: os.path.abspath(os.path.join(os.path.dirname(__file__), *x))
connections = {}
mouse = MouseEvent()

class Room(object):

    def __init__(self, name, clients=[]):
        self.name = name
        self.clients = clients
        print self.clients

    def __repr__(self):
        return self.name

class WebSocket(WebSocketHandler):

    def open(self, ws, ctype):
        print 'WebSocket connection to {}/{} opened from {}'.format(ws, ctype, self.request.remote_ip)
        if ws in connections:
            connections[ws].clients.append((self, ctype))
        else:
            connections[ws] = Room(ws, [(self, ctype)])
        self.room = connections[ws]

    def on_message(self, msg):
        print 'Received message from {}'.format(self.request.remote_ip)
        x, y = msg.split(',')
        mouse.move(float(x), float(y))

    def on_close(self):
        print 'Websocket connection closed'
        for idx, elem in enumerate(self.room.clients):
            if elem[0] == self:
                break
        del self.room.clients[idx]

def main():
    settings = { 'debug': True }
    application = Application([
        (r'/ws/([^/]*)/([^/]*)', WebSocket),
    ], **settings)

    application.listen(address='0.0.0.0', port=8081)
    print 'Started listening at port 8081.'
    IOLoop.instance().start()

if __name__ == '__main__':
    main()