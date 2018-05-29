import configparser
from lib.storage.storage_models import User
from lib.config import commands

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


def write_logging_status_to_config(enabled):
    """
    Writes to config if logging enabled or not
    """

    config['logging'] = {}
    config['logging']['enabled'] = str(enabled)
    with open(CONFIG_NAME, 'w') as configfile:
        config.write(configfile)


def logging_enabled():
    """
    Returns True if logging enabled
    """

    try:
        config.read(CONFIG_NAME)
        level = config['logging']['enabled']
        return level.lower() in ("yes", "true", "t", "1")
    except:
        # write default logging level to config
        write_logging_status_to_config(True)
        return True
