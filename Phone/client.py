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

    _act = lambda self, event_type, x, y: CGEventPost(kCGHIDEventTap, 
        CGEventCreateMouseEvent(None, event_type, (x, y), kCGMouseButtonLeft))

    move = lambda self, x, y: self._act(kCGEventMouseMoved, x, y)

    click = lambda self, x, y: (self._act(kCGEventLeftMouseDown, x, y), self._act(kCGEventLeftMouseUp, x, y))

mouse = MouseEvent()

def on_message(ws, message):
    x, y, event = message.split(',')
    if event == 'move':
        mouse.move(float(x), float(y))
    else:
        mouse.click(float(x), float(y))

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