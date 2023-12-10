import time

from ntropy import measure


@measure(disable_gc=True)
def takes_two_seconds():
    print("slowy")
    time.sleep(2)


takes_two_seconds()
