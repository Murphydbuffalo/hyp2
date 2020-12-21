import json
from uuid import UUID
from http import HTTPStatus
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from hyp.models import Variant, Interaction
from hyp.thompson_sampler import ThompsonSampler


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

    if variant is None:
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
                message="No experiment variants visible to your access token match that ID."
            )

        variant = ThompsonSampler(variants).winner()

        Interaction(
            variant_id=variant["id"],
            experiment_id=experiment_id,
            participant_id=participant_id,
        ).save()

    return apiResponse(payload={
        "id": variant["id"],
        "name": variant["name"]
    })


@csrf_exempt
def record_conversion(request, participant_id, experiment_id):
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
            message="No interaction visible to your access token matches that ID."
        )

    return apiResponse(payload={"id": experiment_id})

# private


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
