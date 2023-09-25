import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from robots.serializer import RobotSerializer
from robots.models import Robot


@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = RobotSerializer(data)

        errors = serializer.errors()
        if not errors:
            serializer.save()
            return JsonResponse({'message': 'Robot created successfully'})
        else:
            return JsonResponse({'errors': errors}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def robot_list(request):
    robots = Robot.objects.all()
    robot_data = [{'model': robot.model, 'version': robot.version} for robot in robots]
    return JsonResponse({'robots': robot_data}, safe=False)