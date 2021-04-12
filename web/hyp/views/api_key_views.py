from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from hyp.models import ApiKey


@login_required
def index(request):
    # TODO: check for permission to view API keys
    api_keys = ApiKey.objects.filter(
        customer_id=request.user.customer_id
    ).order_by('-created_at')

    return render(request, 'hyp/api_keys/index.html', {"api_keys": api_keys})


@login_required
def rotate(request):
    # TODO: check for permission to create API keys
    api_keys = ApiKey.objects.filter(customer_id=request.user.customer_id)
    for api_key in api_keys:
        api_key.deactivated_at = datetime.now()
        api_key.save()

    new_key = ApiKey(customer_id=request.user.customer_id, label=request.POST["api_key_label"])
    new_key.save()

    return redirect("/api_keys/")
