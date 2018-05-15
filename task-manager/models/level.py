import math

class Level:
    def __init__(id, experience=1):
        self.id = id
        self.experience = experience

    def current_level(self):
        return math.floor((-1 + math.sqrt(self.experience * 8 + 1)) / 2)

    def next_level_experience(self):
        level = self.current_level()
        return math.floor((level + 1) * (level + 2) / 2)
