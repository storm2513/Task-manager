class User:
    def __init__(self, email, name, password, level_id=None, id=None):
        self.id = id
        self.email = email
        self.name = name
        self.password = password
        self.level = level_id
