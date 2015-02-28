from Quartz.CoreGraphics import (
    CGEventCreateMouseEvent,
    CGEventPost,
    kCGEventMouseMoved,
    kCGEventLeftMouseDown,
    kCGEventLeftMouseUp,
    kCGMouseButtonLeft,
    kCGHIDEventTap,
    CGEventSetIntegerValueField,
    kCGMouseEventClickState,
    CGEventSetType,
    CFRelease
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

    def double_click(self):
        event = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (self.x, self.y), kCGMouseButtonLeft)
        CGEventSetIntegerValueField(event, kCGMouseEventClickState, 2)
        CGEventPost(kCGHIDEventTap, event)
        CGEventSetType(event, kCGEventLeftMouseUp)
        CGEventPost(kCGHIDEventTap, event)
        CGEventSetType(event, kCGEventLeftMouseDown)
        CGEventPost(kCGHIDEventTap, event)
        CGEventSetType(event, kCGEventLeftMouseUp)
        CGEventPost(kCGHIDEventTap, event)
        #CFRelease(event)

mouse = MouseEvent()
mouse.move(100, 100)
mouse.double_click()