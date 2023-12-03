from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def hello_world(request, variant_number):
    return JsonResponse("Hello World" + " " + str(variant_number), safe = False)