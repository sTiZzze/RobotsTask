from django.db import models

from customers.models import Customer
from orders.enums.RobotEnum import Model, Version


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5,blank=False, null=False)


class DeferredOrder(models.Model):
    customer_id = models.IntegerField(blank=False)
    model = models.CharField(choices=Model.choices(), max_length=2, blank=False, null=False)
    version = models.CharField(choices=Version.choices(), max_length=2, blank=False, null=False)
