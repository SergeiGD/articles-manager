from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.


def index(request):
    return render(request, 'users/users.html', context={
        'hello': 'world',
        'current_page': 'articles',
    })

