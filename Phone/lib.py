# Thanks to http://stackoverflow.com/questions/281133/controlling-the-mouse-from-python-in-os-x
# for inspiration

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