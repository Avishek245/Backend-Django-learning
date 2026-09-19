import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from home.models import contact as ContactMessage


def index(request):
    context = {
        'variable': 'this is sent',
        'variable1': 'this is backend learning'
    }
    return render(request, 'index.html', context)


def about(request):
    return HttpResponse("This is a about page")


def services(request):
    return HttpResponse("This is a service page")


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phnum = request.POST.get('phnum')
        message = request.POST.get('message')

        new_contact = ContactMessage(
            name=name,
            email=email,
            phnum=phnum,
            message=message,
            date=datetime.date.today()
        )
        new_contact.save()
        messages.success(request, "Message has been sent")

    return render(request, 'contact.html')