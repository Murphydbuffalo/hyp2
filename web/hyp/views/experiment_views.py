from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from hyp.models import Experiment


def index(request):
    json = serializers.serialize('json', Experiment.objects.order_by('-created_at'))

    return HttpResponse(json, content_type="application/json")


def show(request, experiment_id):
    experiment = get_object_or_404(Experiment, id=experiment_id)

    return HttpResponse(f'{experiment.name} ({experiment.id})')


def create(request, params):
    return HttpResponse("This is a no-op for now")
