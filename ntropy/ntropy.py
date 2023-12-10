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
            sys.stdout.write("Disabling garbage collection...\n\n")
            gc.disable()

        start = time.perf_counter_ns()

        try:
            return func(*args, **kwargs)
        finally:
            end = time.perf_counter_ns()
            abs_elapsed_time_ns = end - start
            abs_elapsed_time_ms = abs_elapsed_time_ns / 1e6
            time_dict = _build_time_dict(abs_elapsed_time_ms)
            pretty_message: str = _build_time_message(name, time_dict)

            sys.stdout.write(pretty_message)
            sys.stdout.write("\n\n")
            if disable_gc:
                sys.stdout.write("Re-enabling garbage collection...\n")
                gc.enable()

    return wrapper


def _build_time_dict(abs_elapsed_time_ms):
    miliseconds = int(abs_elapsed_time_ms % 1000)

    abs_elapsed_time_sec = abs_elapsed_time_ms // 1e3
    seconds = int(abs_elapsed_time_sec % 60)

    abs_elapsed_time_min = abs_elapsed_time_sec // 60
    minutes = int(abs_elapsed_time_min % 60)

    hours = int(abs_elapsed_time_min // 60)

    return {
        "miliseconds": miliseconds,
        "seconds": seconds,
        "minutes": minutes,
        "hours": hours,
    }


def _build_time_message(func_name, time_dict):
    message = f"The function '{func_name}' took"

    if time_dict["hours"] == 1:
        message += " 1 hour"
    if time_dict["hours"] > 1:
        message += f" {time_dict['hours']} hours"

    if time_dict["minutes"] == 1:
        message += " 1 minute"
    if time_dict["minutes"] > 1:
        message += f" {time_dict['minutes']} minutes"

    if time_dict['seconds'] == 1:
        message += ' 1 seconds'
    if time_dict['seconds'] > 1:
        message += f' {time_dict['seconds']} seconds'

    if time_dict['miliseconds'] == 1:
        message += ' 1 milisecond'
    if time_dict['miliseconds'] > 1:
        message += f' {time_dict['miliseconds']} miliseconds'

    message += ' to run.'

    return message
