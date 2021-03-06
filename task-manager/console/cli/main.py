import os
from cli.arg_parser import handle_commands
import cli.config as config
from tmlib.logger import setup_lib_logging


def main():
    _create_app_data_folder()
    _setup_lib_logging()
    handle_commands()


def _create_app_data_folder():
    if not os.path.exists(config.APP_DATA_DIRECTORY):
        os.makedirs(config.APP_DATA_DIRECTORY)


def _setup_lib_logging():
    log_file_path = os.path.join(
        config.LOGS_DIRECTORY, config.LOG_FILE)
    setup_lib_logging(
        enabled=config.LOGGING_ENABLED,
        log_all_levels=config.LOG_ALL_LEVELS,
        log_file_path=log_file_path,
        log_format=config.LOG_FORMAT)


if(__name__ == "__main__"):
    main()
