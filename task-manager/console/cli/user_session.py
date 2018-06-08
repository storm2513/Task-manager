import configparser
from cli.user import UserStorage


class UserSession:
    def __init__(self, config_file, database_name):
        self.config_file = config_file
        self.config_parser = configparser.ConfigParser()
        self.database_name = database_name


    def login_user(self, username):
        user = UserStorage(self.database_name).get_by_username(username)
        if user is not None:
            self.config_parser['user'] = {}
            self.config_parser['user']['username'] = user.username
            with open(self.config_file, 'w') as configfile:
                self.config_parser.write(configfile)
        return user


    def logout_user(self):
        self.config_parser['user'] = {}
        with open(self.config_file, 'w') as configfile:
            self.config_parser.write(configfile)


    def get_current_user(self):
        username = None
        try:
            self.config_parser.read(self.config_file)
            username = self.config_parser['user']['username']
        except BaseException:
            pass

        return self.login_user(username)
