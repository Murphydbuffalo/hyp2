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

# TODO: namespace under... api/v1?
@csrf_exempt
def variant_assignment(request, participant_id, experiment_id):
    if request.method != "POST":
        return badHTTPMethod()


    token = accessToken(request)

    if not validAccessToken(token):
        return badAccessToken()

    variant = Variant.objects.filter(
        experiment__customer__apikey__access_token=token,
        experiment_id=experiment_id,
        interaction__participant_id=participant_id,
    ).values("id", "name").first()

    if variant == None:
        variants = Variant.objects.filter(
            experiment__customer__apikey__access_token=token,
            experiment_id=experiment_id,
        ).values(
            "id", "name"
        ).annotate(
            num_interactions=Count("interaction"),
            num_conversions=Count(
                "interaction", filter=Q(interaction__converted=True)
            )
        )

        if variants.count() == 0:
            return apiResponse(
                status=404,
                message="No experiment variants found with that ID."
            )

        variant = ThompsonSampler(variants).winner()

        interaction = Interaction(
            variant_id=variant["id"],
            experiment_id=experiment_id,
            participant_id=participant_id,
        ).save()

    return apiResponse(payload={
        "id": variant["id"],
        "name": variant["name"]
    })

@csrf_exempt
def conversion(request, participant_id, experiment_id):
    if request.method not in ["PUT", "PATCH"]:
        return badHTTPMethod()

    token = accessToken(request)

    if not validAccessToken(token):
        return badAccessToken()

    num_rows_updated = Interaction.objects.filter(
        experiment__customer__apikey__access_token=token,
        experiment_id=experiment_id,
        participant_id=participant_id
    ).update(converted=True)

    if num_rows_updated == 0:
        return apiResponse(
            status=404,
            message="No interaction matches that ID."
        )

    return apiResponse(payload={ "id": experiment_id })

def accessToken(request):
    if "X-HYP-TOKEN" not in request.headers.keys():
        return None

    # Clients may send access tokens that are prepended with a namespace like
    # "SANDBOX/" or "PRODUCTION/" to help them know which keys are which.
    return request.headers["X-HYP-TOKEN"].split("/")[-1]

def validAccessToken(token):
    try:
        UUID(str(token), version=4)
        return True
    except ValueError:
        return False

def apiResponse(payload="", status=200, message="success"):
    return HttpResponse(
        json.dumps({
            "payload": payload,
            "message": message,
        }),
        content_type="application/json",
        status=status
    )

def badAccessToken():
    return apiResponse(
        message="Missing or invalid access token.",
        status=HTTPStatus.UNAUTHORIZED
    )

def badHTTPMethod():
    return apiResponse(
        message="That HTTP method isn't supported on this URL.",
        status=HTTPStatus.METHOD_NOT_ALLOWED
    )
