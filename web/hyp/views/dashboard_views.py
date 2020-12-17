import json
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from hyp.models import Experiment, Variant

def index(request):
    json = serializers.serialize('json', Experiment.objects.order_by('-created_at'))

    return HttpResponse(json, content_type="application/json")

def show(request, experiment_id):
    get_object_or_404(Experiment, id=experiment_id)

    return HttpResponse(f'{experiment.name} ({experiment.id})')

def create(request, params):
    return HttpResponse("This is a no-op for now")
