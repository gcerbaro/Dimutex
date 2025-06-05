import requests
import state
from config import NODE_ID, OTHER_NODES
from logger import logger


def send_request_to_all():
    state.increment_clock()
    state.request_clock = state.clock
    logger.info(f"Requesting critical section at clock {state.clock}")
    for node in OTHER_NODES:
        try:
            requests.post(
                f"http://{node}/request",
                json={"node_id": NODE_ID, "clock": state.request_clock},
                timeout=2,
            )
        except Exception as e:
            logger.error(f"Failed to send request to {node}: {e}")


def send_reply(node):
    state.increment_clock()
    try:
        requests.post(
            f"http://{node}/reply",
            json={"node_id": NODE_ID},
            timeout=2,
        )
        logger.info(f"[{NODE_ID}] Sent reply to {node}")
    except Exception as e:
        logger.error(f"[{NODE_ID}] Failed to send reply to {node}: {e}")
