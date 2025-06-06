import time
from state import state
from communication import send_request_to_all
from logger import logger
from config import NODE_ID, OTHER_NODES

def critical_section_loop():
    while True:
        # Simula o processo querendo acessar a CS
        time.sleep(10)

        logger.info(f"[{NODE_ID}] Wanting to enter critical section")
        state.requesting_cs = True
        send_request_to_all()

        # Espera todos os replies
        while not state.got_all_replies(len(OTHER_NODES)):
            time.sleep(1)


        logger.info(f"[{NODE_ID}] Entering critical section")
        # Critical Section
        time.sleep(5)

        logger.info(f"[{NODE_ID}] Exiting critical section")

        state.requesting_cs = False
        state.replies_received.clear()

        # Envia release
        for node in OTHER_NODES:
            try:
                import requests
                requests.post(
                    f"http://{node}/release",
                    json={"node_id": NODE_ID},
                    timeout=2,
                )
            except Exception as e:
                logger.error(f"[{NODE_ID}] Failed to send release to {node}: {e}")
