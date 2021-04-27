from django.shortcuts import render, redirect
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
def create(request):
    # TODO: check for permission to create API keys
    new_key = ApiKey(customer_id=request.user.customer_id, label=request.POST["api_key_label"])
    new_key.save()

    return redirect("/api_keys/")

@login_required
def deactivate(request, api_key_id):
    # TODO: check for permission to retire API keys
    api_key = ApiKey.objects.get(id=api_key_id)
    api_key.deactivated_at = datetime.now()
    api_key.save()

    return redirect("/api_keys/")
