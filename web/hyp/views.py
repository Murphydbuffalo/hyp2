from django.core import serializers
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.db.models import Count, Q
from hyp.models import Experiment, Variant
from hyp.thompson_sampler import ThompsonSampler

# TODO: multiple view files! Multiple model files if possible
# TODO: show fun placeholder GIF? https://media.giphy.com/media/FotYmpcs2kWQ0/giphy.gif
def index(request):
    # TODO: show variants, traffic allocation, conversion rates, lift, precision
    # NBD... JK let's talk to Elias about a design
    json = serializers.serialize('json', Experiment.objects.order_by('-created_at'))

    return HttpResponse(json, content_type="application/json")

def show(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id = experiment_id)
    # TODO: there's a built-in Django shortcut function for this...
    except Experiment.DoesNotExist:
        raise Http404("We couldn't find that experiment 😱")

    return HttpResponse(f'{experiment.name} ({experiment.id})')

def create(request, params):
    return HttpResponse("This is a no-op for now")

# TODO: need authorization
def variant_assignment(request, participant_id, experiment_id):
    variant = Variant.objects.filter(
        interaction__experiment_id=experiment_id,
        interaction__participant_id=participant_id,
    ).values("id", "name").first()

    if variant == None:
        variants = Variant.objects.values("id", "name").filter(
            experiment_id=self.experiment_id
        ).annotate(
            num_interactions=Count("interaction"),
            num_conversions=Count(
                "interaction", filter=Q(interaction__converted=True)
            )
        )

        variant = ThompsonSampler(variants).winner
        interaction = Interaction(
            variant=variant,
            experiment=variant.experiment,
            participant=participant_id
        ).save()

    response = json.dumps({ id: variant.id, name: variant.name })

    return HttpResponse(response, content_type="application/json")

def record_conversion(request, participant_id, experiment_id):
    interaction = Interaction.objects.get(
        experiment_id=experiment_id,
        participant_id=participant_id
    )
    interaction.converted = True
    interaction.save() # TODO: (here and everywhere), handle django.core.exceptions.ValidationError s

    # TODO: let's get all of our JSON responses to adhere to some interface
    # JSON should be an object (I think), so something like:
    # { result: ..., status: ..., error: ... } could be good
    return HttpResponse(json.dumps(True), content_type="application/json")
