from peewee import Model, SqliteDatabase, PrimaryKeyField, CharField, Proxy, DoesNotExist


database_proxy = Proxy()


class UserInstance:
    """
    Class for storing user
    """

    def __init__(self, username, id=None):
        self.id = id
        self.username = username


class User(Model):
    """
    User model
    """

    id = PrimaryKeyField(null=False)
    username = CharField()

    class Meta:
        database = database_proxy


class Adapter:
    def __init__(self, database_name='task_manager'):
        database = SqliteDatabase(database_name)
        database_proxy.initialize(database)
        User.create_table()


class UserStorage(Adapter):
    def create(self, user):
        if self.get_by_username(user.username) is None:
            return self.to_user_instance(User.create(
                id=user.id, username=user.username))

    def delete_by_id(self, user_id):
        User.delete().where(User.id == user_id).execute()

    def get_by_id(self, user_id):
        try:
            return self.to_user_instance(User.get(User.id == user_id))
        except DoesNotExist:
            return None

    def get_by_username(self, username):
        try:
            return self.to_user_instance(User.get(User.username == username))
        except DoesNotExist:
            return None

    def all_users(self):
        return list(map(self.to_user_instance, list(
            User.select(User.id, User.username))))

    def to_user_instance(self, user):
        return UserInstance(id=user.id, username=user.username)
