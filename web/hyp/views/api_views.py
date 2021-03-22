import json
from uuid import UUID
from http import HTTPStatus
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hyp.models import ApiKey, Variant, Interaction
from hyp.thompson_sampler import ThompsonSampler


@csrf_exempt
def variant_assignment(request, participant_id, experiment_id):
    validator = validateRequest(request, allowed_methods=["POST"])
    if validator["success"] is True:
        key = validator["apiKey"]
    else:
        return validator["error"]

    variant = Variant.objects.filter(
        customer_id=key.customer_id,
        experiment_id=experiment_id,
        interaction__participant_id=participant_id,
    ).values("id", "name").first()

    if variant is None:
        variants = Variant.objects.with_interaction_counts().filter(
            customer_id=key.customer_id,
            experiment_id=experiment_id,
        ).values(
            "id", "name", "num_interactions", "num_conversions"
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
            customer_id=key.customer_id,
            participant_id=participant_id,
        ).save()

    return apiResponse(payload={
        "id": variant["id"],
        "name": variant["name"]
    })


@csrf_exempt
def record_conversion(request, participant_id, experiment_id):
    validator = validateRequest(request, allowed_methods=["PUT", "PATCH"])
    if validator["success"] is True:
        key = validator["apiKey"]
    else:
        return validator["error"]

    num_rows_updated = Interaction.objects.filter(
        customer_id=key.customer_id,
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


def validateRequest(request, allowed_methods):
    if request.method not in allowed_methods:
        return {"success": False, "error": badHTTPMethod(), "apiKey": None}

    token = accessToken(request)

    if not validAccessToken(token):
        return {"success": False, "error": badAccessToken(), "apiKey": None}

    key = apiKey(token)

    if key is None:
        return {"success": False, "error": badAccessToken(), "apiKey": None}

    return {"success": True, "apiKey": key, "error": None}


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


def apiKey(token):
    return ApiKey.objects.filter(access_token=token, deactivated_at=None).first()


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
