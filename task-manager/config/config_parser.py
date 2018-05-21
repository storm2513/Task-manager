import configparser
from storage.storage_models import User
from config import commands

CONFIG_NAME = 'config.ini'
config = configparser.ConfigParser()


def authorize_user_from_config():
    try:
        config.read(CONFIG_NAME)
        login = config['user']['email']
        password = config['user']['password']
        commands.login_user(login, password)
    except:
        pass

def write_user_to_config(user):
    config['user'] = {}
    config['user']['email'] = user.email
    config['user']['password'] = user.password
    with open(CONFIG_NAME, 'w') as configfile:
        config.write(configfile)

def remove_user_from_config():
    config['user'] = {}
    with open(CONFIG_NAME, 'w') as configfile:
        config.write(configfile)
