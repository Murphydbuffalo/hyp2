from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from hyp.models import Experiment


@login_required
def index(request):
    # TODO: scope query to user's account
    experiments = Experiment.objects.order_by('-created_at')

    return render(request, 'hyp/experiments/index.html', {"experiments": experiments})


@login_required
def show(request, experiment_id):
    # TODO: scope query to user's account
    experiment = get_object_or_404(Experiment, id=experiment_id)

    return render(request, 'hyp/experiments/show.html', {"experiment": experiment})


@login_required
def create(request, params):
    return HttpResponse("This is a no-op for now")
