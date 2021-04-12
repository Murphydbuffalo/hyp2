from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def show(request):
    return render(request, 'hyp/accounts/profile.html')
