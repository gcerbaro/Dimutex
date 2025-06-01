import time
import threading
from config import NODE_ID, OTHER_NODES
from state import requesting_cs, replies_received, request_clock
from communication import send_request_to_all
import requests

def critical_section_loop():
    global requesting_cs, request_clock
    while True:
        time.sleep(10 + int(NODE_ID[-1]))

        print(f"[{NODE_ID}] Trying to enter critical section...")
        requesting_cs = True
        replies_received.clear()

        send_request_to_all()

        while len(replies_received) < len(OTHER_NODES):
            time.sleep(0.5)

        print(f"[{NODE_ID}] >>> ENTERING CRITICAL SECTION <<<")
        time.sleep(5)
        print(f"[{NODE_ID}] <<< LEAVING CRITICAL SECTION >>>")

        requesting_cs = False
        request_clock = None

        for node in OTHER_NODES:
            try:
                requests.post(
                    f"http://{node}/release",
                    json={"node_id": NODE_ID},
                    timeout=2,
                )
            except Exception as e:
                print(f"[{NODE_ID}] Failed to send release to {node}: {e}")
