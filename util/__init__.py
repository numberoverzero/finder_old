from contextlib import contextmanager
from time import clock


def timer():
    start = clock()
    return lambda: clock() - start


@contextmanager
def timed(func):
    t = timer()
    yield
    delta = t()
    if func:
        func(delta)
