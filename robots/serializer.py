from django.core.exceptions import ValidationError
from robots.models import Robot
import re


class RobotSerializer:

    def __init__(self, data):
        self.data = data

    def is_valid(self):
        try:
            model = self.data['model']
            version = self.data['version']

            if model not in ['R2', '13', 'X5']:
                raise ValidationError('Invalid robot model. Must be in the format "R2", "13", "X5"')
            if version not in ['D2', 'XS', 'LT']:
                raise ValidationError('Invalid robot version. Must be in the format "D2", "XS", "LT"')

            return True
        except Exception:
            return False

    def save(self):
        if self.is_valid():
            model = self.data['model']
            version = self.data['version']
            created = self.data['created']

            robot = Robot(
                serial=model + '-' + version,
                model=model,
                version=version,
                created=created,
            )
            robot.save()
            return robot
        else:
            raise ValidationError('Data is not valid')
