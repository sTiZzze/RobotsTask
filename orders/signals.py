from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from robots.models import Robot
from orders.models import DeferredOrder
from customers.models import Customer
from decouple import config


@receiver(post_save, sender=Robot)
def robot_created(sender, instance, created, **kwargs):
    if created:
        robot = DeferredOrder.objects.filter(model=instance.model, version=instance.version).first()
        if robot:
            customer = Customer.objects.get(id=robot.customer_id)
            subject = 'Ваш заказ'
            message = f'Добрый день! \n\n Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.model}. \n\n Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.'
            from_email = config('EMAIL_HOST_USER')
            recipient_list = [customer.email]
            try:
                with transaction.atomic():
                    send_mail(subject, message, from_email, recipient_list)
                    robot.delete()
            except Exception as e:
                print(f"Ошибка: {e}")