import math


class Level:
    """
    Class for storing User's level. It has experience field on which basis user's level is calculated
    """

    def __init__(self, id, experience=1):
        self.id = id
        self.experience = experience

    def current_level(self):
        """Returns user's current level"""

        return math.floor((-1 + math.sqrt(self.experience * 8 + 1)) / 2)

    def next_level_experience(self):
        """Returns amount of experience required for next level"""

        level = self.current_level()
        return math.floor((level + 1) * (level + 2) / 2)
