import os
from cli.arg_parser import process_args
import config.config as config


def run():
    _create_app_data_folder()
    process_args()


def _create_app_data_folder():
    if not os.path.exists(config.APP_DATA_DIRECTORY):
        os.makedirs(config.APP_DATA_DIRECTORY)


if(__name__ == "__main__"):
    run()
