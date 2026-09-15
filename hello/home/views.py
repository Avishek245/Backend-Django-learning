from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context = {
        'variable':'this is sent',
        'variable1':'this is backend learning'
    }
    return render(request, 'index.html', context)

def about(request):
    return HttpResponse("This is a about page")

def services(request):
    return HttpResponse("This is a service page")

def contact(request):
    return HttpResponse("This is a contact page")