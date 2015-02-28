# Thanks to http://stackoverflow.com/questions/281133/controlling-the-mouse-from-python-in-os-x
# for inspiration

import websocket, subprocess

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
past_img = None

def on_message(ws, message):
    global past_img

    event, data = message.split(',')
    print event
    if event == 'pic':
        try:
            if past_img:
                cmd = """/opt/local/bin/python ./Phone/lib.py {} {}""".format(data, past_img)
                out = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                coords = (out.communicate()[0]).replace('\n', '')
                cx, cy = coords.split(',')
                print cx, cy
                mx = (1280.0 / 480) * float(cx)
                my = (780.0 / 360) * float(cy)
                mouse.move(mx, my)
        except Exception, e:
            print str(e)
        past_img = data
    elif event == 'tap':
        print data
        mouse.click()

def on_error(ws, error):
    print 'Connection error: {}'.format(error)

def on_close(ws):
    print 'Connection Closed'

def on_open(ws):
    print 'Connection opened'
    ws.send('lj')

if __name__ == '__main__':
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp('ws://ec2-52-11-8-41.us-west-2.compute.amazonaws.com:8081/ws/test/laptop',
        on_message=on_message,
        on_error=on_error,
        on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()