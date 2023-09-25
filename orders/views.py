from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from orders.forms import OrderForm
from orders.models import Order


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            robot_model = request.POST.get('robot_model')
            robot_version = request.POST.get('robot_version')
            customer_id = request.POST.get('customer')
        except KeyError as e:
            return JsonResponse({'error': f'Missing key in request: {str(e)}'}, status=400)

        form = OrderForm({'robot_model': robot_model, 'robot_version': robot_version, 'customer': customer_id})
        if form.is_valid():
            Order.objects.create(customer_id=customer_id, robot_serial=robot_model + '-' + robot_version)
            return JsonResponse({'message': 'Заказ размещен'})
        else:
            # Обработка ошибок валидации формы
            errors = form.errors
            return JsonResponse({'error': errors}, status=400)

    return JsonResponse({'error': 'Method not supported'}, status=405)
