from django.shortcuts import render

def home(request):
    """View для главной страницы"""
    return render(request, 'time_site/home.html')