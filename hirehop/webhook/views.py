from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def new_job(request):
    if request.method == 'POST':
        data = request.POST.dict()
        # process the webhook data here
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def invoice_created(request):
    if request.method == 'POST':
        data = request.POST.dict()
        # process the webhook data here
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'})