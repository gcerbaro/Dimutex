import requests
from config import NODE_ID, OTHER_NODES
from logger import logger
from state import state


def send_request_to_all():
    state.increment_clock()
    request_clock = state.get_clock()
    state.set_requesting_cs(True, request_clock=request_clock)
    logger.info(f"{Colors.YELLOW}Requesting critical section at clock {request_clock}")

    for node in OTHER_NODES:
        try:
            requests.post(
                f"http://{node}/request",
                json={"node_id": NODE_ID, "clock": request_clock},
                timeout=2,
            )
        except Exception as e:
            logger.error(f"{Colors.RESET}Failed to send request to {node}: {e}")

def send_reply(node):
    state.increment_clock()
    try:
        requests.post(
            f"http://{node}/reply",
            json={"node_id": NODE_ID},
            timeout=2,
        )
        logger.info(f"{Colors.CYAN}[{NODE_ID}] Sent reply to {node}")
    except Exception as e:
        logger.error(f"{Colors.RESET}[{NODE_ID}] Failed to send reply to {node}: {e}")

class Colors:
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    MAGENTA = "\033[95m"
