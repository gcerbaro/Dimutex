import threading

clock = 0
request_clock = None
requesting_cs = False
replies_received = set()
deferred_replies = set()

lock = threading.Lock()

def increment_clock(received_clock=None):
    global clock
    with lock:
        if received_clock is not None:
            clock = max(clock, received_clock) + 1
        else:
            clock += 1
        return clock
