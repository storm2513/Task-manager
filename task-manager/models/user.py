class User:
    """
    Class for storing user
    """

    def __init__(self, email, name, password, level_id=None, id=None):
        self.id = id
        self.email = email
        self.name = name
        self.password = password
        self.level_id = level_id
