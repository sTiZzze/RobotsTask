from django.urls import path
from robots.views import create_robot, robot_list

urlpatterns = [
    path('create/', create_robot, name='robot-create'),
    path('list/', robot_list, name='robot-list'),
]