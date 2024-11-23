import logging
import os

VALID_LOGGING_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# change the directory accordingly
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def configure_logger(request_id, enabled=True, logging_level='INFO'):
    if logging_level not in VALID_LOGGING_LEVELS:
        logging_level = "INFO"

    logger = logging.getLogger(request_id)
    logger.setLevel(logging_level)

    if not logger.handlers:
        log_file = os.path.join(LOG_DIR, f"{request_id}.log")

        # file hanlder for writing the logs
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging_level)

        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if not enabled:
        logger.disabled = True

    return logger

