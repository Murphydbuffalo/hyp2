from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from os import environ
from hyp_client.v1 import HypClient

def index(request):
    hyp = HypClient(environ.get('HYP_API_TOKEN'))
    user_id = 1
    experiment_id = 12 # landing page graphic experiment
    response = hyp.assignment(participant_id=user_id, experiment_id=experiment_id)
    variant = "Animated screenshot"

    if response["message"] == "success":
        variant = response["payload"]["variant_name"]

    return render(request, 'hyp/landing_pages/home.html', { "variant": variant })
