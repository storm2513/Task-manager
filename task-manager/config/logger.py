import logging

def init_logger(logger_name):
    # logging.basicConfig(filename="log.log", level=logging.INFO)
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(logger_name)
