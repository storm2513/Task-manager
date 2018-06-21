import math
from django.db import models
from django.contrib.auth.models import User


class Level(models.Model):
    TASK_COMPLETED_SCORE = 1  # amount of experience for 1 completed task

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    experience = models.IntegerField(default=0)

    def current_level(self):
        """Returns user's current level"""

        return math.floor((-1 + math.sqrt(self.experience * 8 + 1)) / 2) + 1

    def next_level_experience(self):
        """Returns amount of experience required for next level"""

        level = self.current_level()
        return math.floor((level + 1) * (level + 2) / 2)

    def increase(self):
        self.experience += self.TASK_COMPLETED_SCORE
        self.save()
