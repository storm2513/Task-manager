import configparser
from storage.storage_models import User
from enums.logging_level import LoggingLevel
from config import commands

CONFIG_NAME = 'config.ini'
config = configparser.ConfigParser()


"""
This module provides methods to work with config file
"""


def authorize_user_from_config():
    """
    Reads email and password from config file and tries to login
    """

    try:
        config.read(CONFIG_NAME)
        login = config['user']['email']
        password = config['user']['password']
        commands.login_user(login, password)
    except:
        pass

def write_user_to_config(user):
    """
    Writes to config file user's email and password
    """

    config['user'] = {}
    config['user']['email'] = user.email
    config['user']['password'] = user.password
    with open(CONFIG_NAME, 'w') as configfile:
        config.write(configfile)

def remove_user_from_config():
    """
    Removes user from config
    """

    config['user'] = {}
    with open(CONFIG_NAME, 'w') as configfile:
        config.write(configfile)


def write_logging_level_to_config(level):
    """
    Writes to config file logging level
    """

    config['logging'] = {}
    config['logging']['level'] = str(level)
    with open(CONFIG_NAME, 'w') as configfile:
        config.write(configfile)


def get_logging_level_from_config():
    """
    Returns logging level from config file
    """

    try:
        config.read(CONFIG_NAME)
        level = int(config['logging']['level'])
        return level
    except:
        # write default logging level to config
        write_logging_level_to_config(LoggingLevel.ON.value)
        return LoggingLevel.ON.value
