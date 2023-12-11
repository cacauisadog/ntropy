import gc
import sys
import time
from functools import partial, wraps
from typing import Callable, Literal, Optional, TypedDict


class TimeDict(TypedDict):
    hours: int
    minutes: int
    seconds: int
    miliseconds: int


def measure_time(
    func: Optional[Callable] = None, *, message_format: Literal["human", "complete"] = "human", disable_gc=False
):
    if func is None:
        return partial(measure_time, message_format=message_format, disable_gc=disable_gc)

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
            time_dict: TimeDict = _build_time_dict(abs_elapsed_time_ms)
            pretty_message: str = _build_time_message(name, time_dict, message_format)

            sys.stdout.write(pretty_message)
            sys.stdout.write("\n\n")
            if disable_gc:
                sys.stdout.write("Re-enabling garbage collection...\n")
                gc.enable()

    return wrapper


def _build_time_dict(abs_elapsed_time_ms) -> TimeDict:
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


def _build_time_message(func_name, time_dict: TimeDict, message_format):
    if message_format == "human":
        return _build_human_friendly_time_message(func_name, time_dict)

    return _build_complete_time_message(func_name, time_dict)


def _build_human_friendly_time_message(func_name, time_dict: TimeDict):
    message = f"The function '{func_name}' took"
    time_taken_message = ""

    if time_dict["hours"] == 1:
        time_taken_message += " 1 hour"
    if time_dict["hours"] > 1:
        time_taken_message += f" {time_dict['hours']} hours"

    if time_dict["minutes"] == 1:
        time_taken_message += " 1 minute"
    if time_dict["minutes"] > 1:
        time_taken_message += f" {time_dict['minutes']} minutes"

    if time_dict["seconds"] == 1:
        time_taken_message += " 1 second"
    if time_dict["seconds"] > 1:
        time_taken_message += f" {time_dict['seconds']} seconds"

    if time_dict["miliseconds"] == 1:
        time_taken_message += " 1 milisecond"
    if time_dict["miliseconds"] > 1:
        time_taken_message += f" {time_dict['miliseconds']} miliseconds"

    # if nothing matched, it means that the function took less than a fraction of a milisecond to run
    if len(time_taken_message) == 0:
        time_taken_message = " less than one milisecond"

    full_message = message + time_taken_message + " to run."

    return full_message


def _build_complete_time_message(func_name, time_dict: TimeDict):
    message = f"The function '{func_name}' took"
    time_taken_message = (
        f"{time_dict['hours']}hr {time_dict['minutes']}min {time_dict['seconds']}sec {time_dict['miliseconds']}ms"
    )

    full_message = message + " " + time_taken_message + " to run."
    return full_message
