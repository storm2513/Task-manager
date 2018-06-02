import logging
import os

"""This module provides functions to work with logging"""

def setup_lib_logging(
        enabled=True,
        log_all_levels=True,
        log_file_path='./log.log',
        log_format='%(asctime)s, %(name)s, [%(levelname)s]: %(message)s'):
    def check_and_create_logger_file(path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        try:
            open(path, 'r').close()
        except FileNotFoundError:
            open(path, 'w').close()

    check_and_create_logger_file(log_file_path)
    formatter = logging.Formatter(log_format)

    file_logging_handler = logging.FileHandler(log_file_path)
    if log_all_levels:
        file_logging_handler.setLevel(logging.DEBUG)
    else:
        file_logging_handler.setLevel(logging.WARNING)
    file_logging_handler.setFormatter(formatter)
    logger = get_logger()
    logger.setLevel(logging.DEBUG)
    if (logger.hasHandlers()):
        logger.handlers.clear()

    if enabled:
        logger.disabled = False
        logger.addHandler(file_logging_handler)
    else:
        logger.disabled = True


def get_logger():
    return logging.getLogger('task manager logger')
