import time
from state import state
from communication import send_request_to_all
from logger import logger
from config import NODE_ID, OTHER_NODES
from communication import colors

def critical_section_loop():
    while True:
        # Simula o processo querendo acessar a CS
        time.sleep(10)

        logger.info(f"{colors.RED}[{NODE_ID}] Wanting to enter critical section")
        state.requesting_cs = True
        send_request_to_all()

        # Espera todos os replies
        wait_start = time.time()
        TIMEOUT = 20

        while len(state.replies_received) < len(OTHER_NODES):
            if time.time() - wait_start > TIMEOUT:
                logger.warning(f"{colors.MAGENTA}[{NODE_ID}] Timeout waiting for replies")
                break
            time.sleep(1)



        logger.info(f"{colors.RED}[{NODE_ID}] Entering critical section")
        # Critical Section
        time.sleep(5)

        logger.info(f"{colors.RED}[{NODE_ID}] Exiting critical section")

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
                logger.error(f"{colors.RESET}[{NODE_ID}] Failed to send release to {node}: {e}")
