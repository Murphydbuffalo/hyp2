from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from hyp.models import Experiment


@login_required
def index(request):
    # TODO: scope query to user's account
    json = serializers.serialize('json', Experiment.objects.order_by('-created_at'))

    return HttpResponse(json, content_type="application/json")


@login_required
def show(request, experiment_id):
    experiment = get_object_or_404(Experiment, id=experiment_id)

    return HttpResponse(f'{experiment.name} ({experiment.id})')


@login_required
def create(request, params):
    return HttpResponse("This is a no-op for now")
