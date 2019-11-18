from django.shortcuts import render
from django.http import HttpResponse
from listings.choices import receiver_choices

# Create your views here.

def index(request):
    context = {
        'receiver_choices':receiver_choices,
    }
    return render(request, 'pages/index.html',context)

def about(request):
    return render(request, 'pages/about.html')
