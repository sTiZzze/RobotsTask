from django import forms
from django.core.exceptions import ValidationError

from robots.models import Robot
from customers.models import Customer
from orders.models import DeferredOrder


class OrderForm(forms.Form):
    MODEL_CHOICES = ['R2', '13', 'X5']
    VERSION_CHOICES = ['D2', 'XS', 'LT']

    customer = forms.IntegerField(required=True)
    robot_model = forms.CharField(max_length=100)
    robot_version = forms.CharField(max_length=100)

    def clean_robot_model(self):
        robot_model = self.cleaned_data['robot_model']
        if robot_model not in self.MODEL_CHOICES:
            raise ValidationError(f'Invalid robot model. Must be one of {", ".join(self.MODEL_CHOICES)}')
        return robot_model

    def clean_robot_version(self):
        robot_version = self.cleaned_data['robot_version']
        if robot_version not in self.VERSION_CHOICES:
            raise ValidationError(f'Invalid robot version. Must be one of {", ".join(self.VERSION_CHOICES)}')
        return robot_version

    def clean(self):
        cleaned_data = super().clean()
        robot_model = cleaned_data.get('robot_model')
        robot_version = cleaned_data.get('robot_version')
        customer_id = cleaned_data.get('customer')

        # Проверка существования клиента
        if not Customer.objects.filter(id=customer_id).exists():
            raise ValidationError('Неверный идентификатор клиента')

        # Проверка существования робота
        robot = Robot.objects.filter(model=robot_model, version=robot_version)
        if not robot:
            DeferredOrder.objects.create(customer_id=customer_id, model=robot_model, version=robot_version)
            raise ValidationError(
                'Извините, выбранный вами робот временно недоступен. Мы уведомим вас, когда он появится в наличии.')
        return cleaned_data