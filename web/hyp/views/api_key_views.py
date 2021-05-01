from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from hyp.models import ApiKey


@login_required
def index(request):
    if request.user.has_perm("hyp.view_apikey"):
        api_keys = ApiKey.objects.filter(
            customer_id=request.user.customer_id
        ).order_by('-created_at')

        return render(request, 'hyp/api_keys/index.html', {"api_keys": api_keys})
    else:
        raise PermissionDenied


@login_required
def create(request):
    if request.user.has_perm("hyp.add_apikey"):
        new_key = ApiKey(customer_id=request.user.customer_id, label=request.POST["api_key_label"])
        new_key.save()

        return redirect("/api_keys/")
    else:
        raise PermissionDenied


@login_required
def deactivate(request, api_key_id):
    if request.user.has_perm("hyp.change_apikey"):
        api_key = get_object_or_404(ApiKey, id=api_key_id)
        api_key.deactivated_at = timezone.now()
        api_key.save()

        return redirect("/api_keys/")
    else:
        raise PermissionDenied
