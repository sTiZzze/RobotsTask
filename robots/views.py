from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from robots.serializer import RobotSerializer


@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = RobotSerializer(data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Robot created successfully'})
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)