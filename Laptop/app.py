import os, uuid

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler
from tornado.escape import json_encode, json_decode

rel = lambda *x: os.path.abspath(os.path.join(os.path.dirname(__file__), *x))
connections = {}

class Room(object):

    def __init__(self, name, clients=[]):
        self.name = name
        self.clients = clients
        print self.clients

    def __repr__(self):
        return self.name

class IndexHandler(RequestHandler):

    def get(self):
        room = str(uuid.uuid4().get_hex().upper()[0:6])
        self.redirect('/room/' + room)

class RoomHandler(RequestHandler):

    def get(self, room):
        self.render('room.html')

class WebSocket(WebSocketHandler):

    def open(self, ws, ctype):
        print 'WebSocket connection to {}/{} opened from {}'.format(ws, ctype, self.request.remote_ip)
        if ws in connections:
            for client, client_type in connections[ws].clients:
                if client_type == 'browser' and ctype == 'laptop':
                    client.write_message(json_encode({'msg': 'lj'}))

            connections[ws].clients.append((self, ctype))
        else:
            connections[ws] = Room(ws, [(self, ctype)])
        self.room = connections[ws]

    def on_message(self, msg):
        print 'Received message from {}'.format(self.request.remote_ip)
        data = json_decode(msg)
        if data['msg'] == 'frame':
            person = 'laptop' if data['get'] else 'browser'
            for client, ctype in self.room.clients:
                if ctype == person:
                    client.write_message(msg)
        else:
            print data

    def on_close(self):
        print 'Websocket connection closed'
        for idx, elem in enumerate(self.room.clients):
            if elem[0] == self:
                break
        del self.room.clients[idx]

def main():
    settings = dict(
        template_path=rel('templates'),
        static_path=rel('static'),
        debug=True
    )

    application = Application([
        (r'/', IndexHandler),
        (r'/room/([^/]*)', RoomHandler),
        (r'/ws/([^/]*)/([^/]*)', WebSocket),
    ], **settings)

    application.listen(address='0.0.0.0', port=8080)
    print 'Started listening at port 8080.'
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
