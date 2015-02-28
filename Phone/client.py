# Thanks to http://stackoverflow.com/questions/281133/controlling-the-mouse-from-python-in-os-x
# for inspiration

import websocket

from Quartz.CoreGraphics import (
    CGEventCreateMouseEvent,
    CGEventPost,
    kCGEventMouseMoved,
    kCGEventLeftMouseDown,
    kCGEventLeftMouseDown,
    kCGEventLeftMouseUp,
    kCGMouseButtonLeft,
    kCGHIDEventTap
)

class MouseEvent(object):

    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y

    def _act(self, event_type, x=None, y=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        CGEventPost(kCGHIDEventTap, 
            CGEventCreateMouseEvent(None, event_type, (x, y), kCGMouseButtonLeft))

    def move(self, x, y):
        self._act(kCGEventMouseMoved, x, y)
        self.set(x, y)

    click = lambda self: (self._act(kCGEventLeftMouseDown), self._act(kCGEventLeftMouseUp))

mouse = MouseEvent()

def on_message(ws, message):
    x, y, event = message.split(',')
    if event == 'move':
        mouse.move(float(x), float(y))
    else:
        mouse.click()

def on_error(ws, error):
    print 'Connection error: {}'.format(error)

def on_close(ws):
    print 'Connection Closed'

def on_open(ws):
    print 'Connection opened'

if __name__ == '__main__':
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp('ws://ec2-52-11-8-41.us-west-2.compute.amazonaws.com:8081/ws/test/laptop',
        on_message=on_message,
        on_error=on_error,
        on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()