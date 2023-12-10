import gc
import sys
import time
from functools import partial, wraps
from typing import Callable


def measure(func: Callable = None, *, disable_gc=False):
    if func is None:
        return partial(measure, disable_gc=disable_gc)

    name = func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        if disable_gc:
            sys.stdout.write("Disabling garbage collection...\n")
            gc.disable()

        start = time.perf_counter_ns()

        try:
            return func(*args, **kwargs)
        finally:
            end = time.perf_counter_ns()
            elapsed_time_ns = end - start
            sys.stdout.write(f"{name} function took {str(elapsed_time_ns)} ns to run")
            sys.stdout.write("\n")
            if disable_gc:
                sys.stdout.write("Re-enabling garbage collection...\n")
                gc.enable()

    return wrapper
