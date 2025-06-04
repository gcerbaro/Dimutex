import os
import colorlog
import logging

def setup_logger():
    NODE_ID = os.environ.get("NODE_ID", "unknown")  # <- Pega o ID do container
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        f"%(log_color)s%(asctime)s [{NODE_ID}] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    ))

    logger = colorlog.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers = [handler]

    return logger

logger = setup_logger()
