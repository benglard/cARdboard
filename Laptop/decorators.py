import threading

def set_interval_helper(func, sec):
    def func_wrapper():
        set_interval_helper(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

class set_interval(object):
    def __init__(self, sec): self.delay = sec
    def __call__(self, func): set_interval_helper(func, self.delay)