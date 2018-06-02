class BaseController:
    """Base class for all controllers"""

    def __init__(self, user_id, storage):
        self.user_id = user_id
        self.storage = storage
