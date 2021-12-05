import json
from uuid import UUID
from http import HTTPStatus
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hyp.models import Variant, Interaction
from hyp.thompson_sampler import ThompsonSampler


@csrf_exempt
def variant_assignment(request, participant_id, experiment_id):
    validator = validateRequest(request, allowed_methods=["POST"])
    if validator["success"] is True:
        token = validator["access_token"]
    else:
        return validator["error"]

    variants = Variant.objects.for_assignment(
        access_token=token,
        participant_id=participant_id,
        experiment_id=experiment_id
    )

    if len(variants) == 0:
        return apiResponse(
            status=404,
            message="No experiment with that ID was found."
        )

    already_assigned_variant = next((v for v in variants if v.interaction_id is not None), None)

    if already_assigned_variant is None:
        variant = ThompsonSampler(variants).winner()
        customer_id = variants[0].customer_id

        Interaction(
            variant_id=variant.id,
            experiment_id=experiment_id,
            customer_id=customer_id,
            participant_id=participant_id,
        ).save()

    else:
        variant = already_assigned_variant

    return apiResponse(payload={
        "variant_id": variant.id,
        "variant_name": variant.name
    })


@csrf_exempt
def record_conversion(request, participant_id, experiment_id):
    validator = validateRequest(request, allowed_methods=["PUT", "PATCH"])
    if validator["success"] is True:
        token = validator["access_token"]
    else:
        return validator["error"]

    Interaction.objects.record_conversion(
        access_token=token,
        experiment_id=experiment_id,
        participant_id=participant_id
    )

    return apiResponse(payload={"id": experiment_id})

# private


def validateRequest(request, allowed_methods):
    if request.method not in allowed_methods:
        return {"success": False, "error": badHTTPMethod(), "apiKey": None}

    token = accessToken(request)

    if not validAccessToken(token):
        return {"success": False, "error": badAccessToken(), "apiKey": None}

    return {"success": True, "access_token": token, "error": None}


def accessToken(request):
    if "X-HYP-TOKEN" not in request.headers.keys():
        return None

    # Clients may send access tokens that are prepended with a namespace like
    # "SANDBOX/HYP/" or "PRODUCTION/HYP/" to help them know which keys are which.
    return request.headers["X-HYP-TOKEN"].split("/")[-1]


def validAccessToken(token):
    if token is None:
        return False

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
