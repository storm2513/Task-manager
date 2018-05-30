import logging
import os
import config.config as config


def setup_logging(logger):
    high_level_log_file_path = os.path.join(
        config.LOGS_DIRECTORY, config.HIGH_LEVEL_LOG_NAME)
    low_level_log_file_path = os.path.join(
        config.LOGS_DIRECTORY, config.LOW_LEVEL_LOG_NAME)

    def check_and_create_logger_files(path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        try:
            open(path, 'r').close()
        except FileNotFoundError:
            open(path, 'w').close()

    check_and_create_logger_files(high_level_log_file_path)
    check_and_create_logger_files(low_level_log_file_path)
    formatter = logging.Formatter(config.LOGGING_FORMATTER)

    file_high_logging_handler = logging.FileHandler(high_level_log_file_path)
    file_high_logging_handler.addFilter(HighLoggingFilter())
    file_high_logging_handler.setLevel(logging.DEBUG)
    file_high_logging_handler.setFormatter(formatter)

    file_low_logging_handler = logging.FileHandler(low_level_log_file_path)
    file_low_logging_handler.addFilter(LowLoggingFilter())
    file_low_logging_handler.setLevel(logging.DEBUG)
    file_low_logging_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)

    if (logger.hasHandlers()):
        logger.handlers.clear()

    if config.LOGGING_ENABLED:
        logger.disabled = False
        logger.addHandler(file_high_logging_handler)
        logger.addHandler(file_low_logging_handler)
    else:
        logger.disabled = True


def get_logger(name):
    logger = logging.getLogger(name)
    setup_logging(logger)
    return logger


class LowLoggingFilter(logging.Filter):
    def filter(self, record):
        return record.levelno <= logging.INFO


class HighLoggingFilter(logging.Filter):
    def filter(self, record):
        return record.levelno > logging.INFO
