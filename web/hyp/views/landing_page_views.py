from django.shortcuts import render


def index(request):
    return render(request, 'hyp/landing_pages/home.html', {})
