from django.core.exceptions import ValidationError
from robots.models import Robot
from datetime import datetime
import traceback


class RobotSerializer:

    def __init__(self, data):
        self.data = data

    def errors(self):
        try:
            model = self.data['model']
            version = self.data['version']
            created = self.data['created']

            try:
                datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValidationError('Invalid datetime format. Must be in the format "YYYY-MM-DD HH:MM:SS"')

            if model not in ['R2', '13', 'X5']:
                raise ValidationError('Invalid robot model. Must be in the format "R2", "13", "X5"')

            if version not in ['D2', 'XS', 'LT']:
                raise ValidationError('Invalid robot version. Must be in the format "D2", "XS", "LT"')

            return False
        except Exception as e:
            return str(e)

    def save(self):
        if not self.errors():
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
