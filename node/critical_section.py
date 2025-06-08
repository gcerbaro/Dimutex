import time
from state import state
from communication import send_request_to_all, send_reply
from logger import logger, Colors
from config import NODE_ID, OTHER_NODES
import requests

SHARED_DATA_URL = "http://shared-data-container:6000/data"

def access_shared_data():
    try:
        logger.info(f"{Colors.BLUE}[{NODE_ID}] Editing data...")
        res = requests.get(SHARED_DATA_URL)
        data = res.json()

        new_value = data["value"] + 1
        res = requests.post(SHARED_DATA_URL, json={"value": new_value})
        logger.info(f"{Colors.BLUE}[{NODE_ID}] Data Edited Succesfully!")
    except Exception as e:
        logger.error(f"[{NODE_ID}] Error Accessing Shared Data: {e}")


def critical_section_loop():
    while True:
        # Simula o processo querendo acessar a CS
        time.sleep(10)

        logger.info(f"{Colors.YELLOW}[{NODE_ID}] Wanting to enter critical section")

        # Atualiza o clock e marca intenção de acessar a CS
        state.increment_clock()
        request_clock = state.get_clock()
        state.set_requesting_cs(True, request_clock)
        send_request_to_all()

        # Espera todos os replies
        #wait_start = time.time()
        #TIMEOUT = 20
        while(True):
            if(state.got_all_replies(len(OTHER_NODES))):
                state.set_in_cs(True)
                logger.info(f"{Colors.RED}[{NODE_ID}] Entering critical section")
                break

        # Seção Crítica
        access_shared_data()
        time.sleep(5)

        logger.info(f"{Colors.RED}[{NODE_ID}] Exiting critical section")
        state.set_in_cs(False)

        # Marca que não está mais solicitando CS
        state.set_requesting_cs(False)
        state.clear_replies()

        # Envia replies pendentes
        with state.lock:
            deferred = list(state.deferred_replies)
            state.deferred_replies.clear()

        for node_id in deferred:
            try:
                send_reply(node_id + ":5000")
            except Exception as e:
                logger.error(f"{Colors.RESET}[{NODE_ID}] Failed to send deferred reply to {node_id}: {e}")
