# main_app/views.py

from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'main_app/home.html',context)
