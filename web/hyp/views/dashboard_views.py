import json
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from hyp.models import Experiment, Variant

# TODO: show fun placeholder GIF? https://media.giphy.com/media/FotYmpcs2kWQ0/giphy.gif
# TODO: Server sends back HTML for the dashboard, but we load up React for
# interaction-heavy stuff, so will want to set up Webpack + React at some point
def index(request):
    # TODO: let's build some HTML instead
    # TODO: let's include variants
    json = serializers.serialize('json', Experiment.objects.order_by('-created_at'))

    return HttpResponse(json, content_type="application/json")

def show(request, experiment_id):
    get_object_or_404(Experiment, id=experiment_id)

    return HttpResponse(f'{experiment.name} ({experiment.id})')

def create(request, params):
    return HttpResponse("This is a no-op for now")
