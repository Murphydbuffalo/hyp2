import json
from http import HTTPStatus
from uuid import UUID
from django.core import serializers
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Count, Q
from hyp.models import Experiment, Variant, Interaction
from hyp.thompson_sampler import ThompsonSampler

# TODO: multiple view files! Multiple model files if possible
# TODO: show fun placeholder GIF? https://media.giphy.com/media/FotYmpcs2kWQ0/giphy.gif
# TODO: Server sends back HTML for the dashboard, but we load up React for
# interaction-heavy stuff, so will want to set up Webpack + React at some point
def index(request):
    json = serializers.serialize('json', Experiment.objects.order_by('-created_at'))

    return HttpResponse(json, content_type="application/json")

def show(request, experiment_id):
    get_object_or_404(Experiment, id=experiment_id)

    return HttpResponse(f'{experiment.name} ({experiment.id})')

def create(request, params):
    return HttpResponse("This is a no-op for now")

# TODO: need authorization... accept API token from header, check signature?
# Then if good, scope queries to that API key? First step redundant?
# Could denormalize to put ApiKey or Customer on every model so that we don't
# have to do crazy joins to do variant assignment. May well be worth the performance
# lift because this endpoint needs to be fast...
#
# TODO: namespace under... api/v1?
# TODO: strip out PRODUCTION/SANDBOX prefix from access tokens
@csrf_exempt
def variant_assignment(request, participant_id, experiment_id):
    if request.method != "POST":
        return HttpResponse(
            content_type="application/json",
            status=HTTPStatus.METHOD_NOT_ALLOWED
        )

    if invalidAccessToken(request):
        return HttpResponse(
            "Missing or invalid access token.",
            content_type="application/json",
            status=HTTPStatus.UNAUTHORIZED
        )

    variant = Variant.objects.filter(
        experiment__customer__apikey__access_token=request.headers["X-HYP-TOKEN"],
        experiment_id=experiment_id,
        interaction__participant_id=participant_id,
    ).values("id", "name").first()

    if variant == None:
        # TODO: custom 404 and 500 handlers for API endpoints
        # (as opposed to non-api, HTML serving endpoints)
        # https://stackoverflow.com/questions/17662928/django-creating-a-custom-500-404-error-page
        variants = get_list_or_404(
            Variant.objects.filter(
                experiment__customer__apikey__access_token=request.headers["X-HYP-TOKEN"],
                experiment_id=experiment_id,
            ).values(
                "id", "name"
            ).annotate(
                num_interactions=Count("interaction"),
                num_conversions=Count(
                    "interaction", filter=Q(interaction__converted=True)
                )
            )
        )

        variant = ThompsonSampler(variants).winner()

        interaction = Interaction(
            variant_id=variant["id"],
            experiment_id=experiment_id,
            participant_id=participant_id,
        ).save()

    response = json.dumps({ "id": variant["id"], "name": variant["name"] })

    return HttpResponse(response, content_type="application/json")

@csrf_exempt
def conversion(request, participant_id, experiment_id):
    if request.method not in ["PUT", "PATCH"]:
        return HttpResponse(
            content_type="application/json",
            status=HTTPStatus.METHOD_NOT_ALLOWED
        )

    if invalidAccessToken(request):
        return HttpResponse(
            "Missing or invalid access token.",
            content_type="application/json",
            status=HTTPStatus.UNAUTHORIZED
        )

    num_rows_updated = Interaction.objects.filter(
        experiment__customer__apikey__access_token=request.headers["X-HYP-TOKEN"],
        experiment_id=experiment_id,
        participant_id=participant_id
    ).update(converted=True)

    if num_rows_updated == 0:
        raise Http404("No interaction matches the given query.")

    # TODO: let's get all of our JSON responses to adhere to some interface
    # JSON should be an object (I think), so something like:
    # { result: ..., status: ..., error: ... } could be good
    return HttpResponse(json.dumps(True), content_type="application/json")

# TODO: endpoints to ask questions about specific experiments such as:
# 1. What's the current split of traffic? Can get a good estimate by running the
# Thompson Sampler 1000 times or so
# 2. What's the conversion rate for each variant?
# 3. Can we be confident in the winner? So need some measure of the *precision*
# of our prediction of the optimal variant. The narrower the interval of the HDPI
# the better, find some way to communicate that narrowness to the user as a
# score out of 100.
# 4. Post-MVP, what's the value-add of the variants? (based on user defined value
# of conversions)
# 5. Post-MVP, what's the grid approximate posterior for each variant? Mayyybe
# do this, most people won't know or care about this

# TODO: endpoints to query the list of experiments:
# 1. I want to filter by active vs inactive
# 2. I want to order by value-add
# 3. I want to order by conversion rate
# 4. I want to order by confidence in winner

# TODO: endpoints to modify experiments
# 1. I want to mark as active or inactive. How to handle this? Return an error
# any time they try get a participant assignment or do a conversion? Or gracefully
# handle by still performing assignments but returning warnings that no conversion
# are being recorded? Maybe always return the default variant? Should we make the
# user mark one variant as the default? I'd rather not... Let's talk to Elias.
# 2. I want to provide a baseline guesstimate of the conversion rate for a given
# feature. Maybe Hyp can provide reasonable, industry standard conversion rates
# for common types of things like marketing emails vs personal notifications.
# Use these to supply a prior to the Thompson Sampler. How to do that?

def invalidAccessToken(request):
    if "X-HYP-TOKEN" not in request.headers.keys():
        return True

    try:
        UUID(str(request.headers["X-HYP-TOKEN"]), version=4)
        return False
    except ValueError:
        return True
