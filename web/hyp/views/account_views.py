from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def show(request):
    access_token = request.user.customer.apikey_set.active()

    return render(request, 'hyp/accounts/profile.html', context={'access_token': access_token})
