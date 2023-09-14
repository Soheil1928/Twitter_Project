from django.shortcuts import render


def home(request):
    return render(request, 'twitter/home_page.html')
