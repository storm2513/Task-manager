from cli.user import UserStorage
from cli.config.config_parser import get_username_from_config, remove_user_from_config, write_user_to_config


def login_user(username):
    user = UserStorage().get_by_username(username)
    if user is not None:
        write_user_to_config(user)
    return user


def current_user():
    return authorize_user_from_config()


def logout_user():
    remove_user_from_config()


def authorize_user_from_config():
    return login_user(get_username_from_config())
