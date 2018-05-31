import logging
import os
import config.config as config


def setup_logging(logger):
    log_file_path = os.path.join(
        config.LOGS_DIRECTORY, config.LOG_FILE)

    def check_and_create_logger_files(path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        try:
            open(path, 'r').close()
        except FileNotFoundError:
            open(path, 'w').close()

    check_and_create_logger_files(log_file_path)
    formatter = logging.Formatter(config.LOGGING_FORMATTER)

    file_logging_handler = logging.FileHandler(log_file_path)
    if config.LOGGING_ALL_LEVELS:
        file_logging_handler.setLevel(logging.DEBUG)
    else:
        file_logging_handler.setLevel(logging.WARNING)
    file_logging_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)

    if (logger.hasHandlers()):
        logger.handlers.clear()

    if config.LOGGING_ENABLED:
        logger.disabled = False
        logger.addHandler(file_logging_handler)
    else:
        logger.disabled = True
    return logger

def get_logger(name):
    logger = logging.getLogger(name)
    return setup_logging(logger)
