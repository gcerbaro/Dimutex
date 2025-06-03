import requests
from config import NODE_ID, OTHER_NODES
from state import increment_clock, clock, request_clock
from logger import logger

def send_request_to_all():
    increment_clock()
    from state import request_clock  # Atualiza valor global
    request_clock = clock
    logger.info(f"Requesting critical section at clock {clock}")
    for node in OTHER_NODES:
        try:
            requests.post(
                f"http://{node}/request",
                json={"node_id": NODE_ID, "clock": request_clock},
                timeout=2,
            )
        except Exception as e:
            logger.error(f"Failed to send request to {node}: {e}")

def send_reply(node):
    try:
        requests.post(
            f"http://{node}/reply",
            json={"node_id": NODE_ID},
            timeout=2,
        )
        logger.info(f"[{NODE_ID}] Sent reply to {node}")
    except Exception as e:
        logger.error(f"[{NODE_ID}] Failed to send reply to {node}: {e}")


