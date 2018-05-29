import configparser
from cli.user import UserInstance as User
from lib.config import commands


CONFIG_NAME = 'config.ini'
config = configparser.ConfigParser()


"""
This module provides methods to work with config file
"""


def get_username_from_config():
    try:
        config.read(CONFIG_NAME)
        username = config['user']['username']
        return username
    except:
        pass


def write_user_to_config(user):
    config['user'] = {}
    config['user']['username'] = user.username
    with open(CONFIG_NAME, 'w') as configfile:
        config.write(configfile)


def remove_user_from_config():
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
    try:
        config.read(CONFIG_NAME)
        level = config['logging']['enabled']
        return level.lower() in ("yes", "true", "t", "1")
    except:
        # logging is enabled by default
        write_logging_status_to_config(True)
        return True
