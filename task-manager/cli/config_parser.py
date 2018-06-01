import configparser
from cli.user import UserInstance as User
import cli.config as config
from lib import commands


config_parser = configparser.ConfigParser()


"""
This module provides methods to work with config file
"""


def get_username_from_config():
    try:
        config_parser.read(config.CONFIG_FILE)
        username = config_parser['user']['username']
        return username
    except BaseException:
        pass


def write_user_to_config(user):
    config_parser['user'] = {}
    config_parser['user']['username'] = user.username
    with open(config.CONFIG_FILE, 'w') as configfile:
        config_parser.write(configfile)


def remove_user_from_config():
    config_parser['user'] = {}
    with open(config.CONFIG_FILE, 'w') as configfile:
        config_parser.write(configfile)
