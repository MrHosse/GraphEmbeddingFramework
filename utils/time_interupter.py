from contextlib import contextmanager
import threading
import _thread


# TODO: fix
class TimeoutException(Exception):
    def __init__(self, msg=''):
        self.msg = msg

@contextmanager
def time_limit(seconds):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    finally:
        timer.cancel()
        print('NO')

def func():
     print("Hello")

import time
with time_limit(5):
    time.sleep(2)