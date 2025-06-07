import threading

class NodeState:
    def __init__(self):
        self.clock = 0
        self.request_clock = None
        self.requesting_cs = False
        self.in_cs = False
        self.replies_received = set()
        self.deferred_replies = set()
        self.lock = threading.Lock()
        


    def increment_clock(self, received_clock=None):
        with self.lock:
            if received_clock is not None:
                self.clock = max(self.clock, received_clock) + 1
            else:
                self.clock += 1
            return self.clock

    def set_requesting_cs(self, value, request_clock=None):
        with self.lock:
            self.requesting_cs = value
            if value:
                self.request_clock = request_clock
            else:
                self.request_clock = None

    def get_request_state(self):
        with self.lock:
            return self.requesting_cs, self.request_clock
        
    def set_in_cs(self, value: bool):
        with self.lock:
            self.in_cs = value


    def add_reply(self, sender_id):
        with self.lock:
            self.replies_received.add(sender_id)

    def got_all_replies(self, expected_count):
        with self.lock:
            return len(self.replies_received) >= expected_count

    def clear_replies(self):
        with self.lock:
            self.replies_received.clear()

    def defer_reply(self, sender_id):
        with self.lock:
            self.deferred_replies.add(sender_id)

    def pop_deferred_reply(self, sender_id):
        with self.lock:
            if sender_id in self.deferred_replies:
                self.deferred_replies.remove(sender_id)
                return True
            return False

    def get_clock(self):
        with self.lock:
            return self.clock

# Instância global
state = NodeState()
