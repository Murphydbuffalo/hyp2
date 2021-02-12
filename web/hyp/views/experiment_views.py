from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from hyp.models import Experiment


@login_required
def index(request):
    experiments = Experiment.objects.filter(
        customer_id=request.user.customer_id
    ).order_by('-created_at')

    return render(request, 'hyp/experiments/index.html', {"experiments": experiments})


@login_required
def show(request, experiment_id):
    experiment = get_object_or_404(
        Experiment, id=experiment_id, customer_id=request.user.customer_id
    )

    return render(request, 'hyp/experiments/show.html', {"experiment": experiment})


@login_required
def create(request, params):
    return HttpResponse("This is a no-op for now")
