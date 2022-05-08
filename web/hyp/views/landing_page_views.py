from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from os import environ
from hyp_client.v1 import HypClient
from uuid import uuid4

def index(request):
    hyp = HypClient(environ.get('HYP_API_TOKEN'))
    participant_id = get_participant_id(request)
    variant = hyp.try_assignment(
        participant_id=participant_id,
        experiment_id=12,
        fallback="Animated screenshot"
    )

    response = render(request, 'hyp/landing_pages/home.html', { "variant": variant })
    response.set_cookie("hyp_participant_id", participant_id, max_age=31536000)

    return response

def get_participant_id(request):
    cookie_participant_id = request.COOKIES.get("hyp_participant_id")

    # Don't let signed up users participate in an experiment about signing up
    if request.user.is_authenticated:
        return None
    elif cookie_participant_id is not None:
        return cookie_participant_id
    else:
        return uuid4().hex
