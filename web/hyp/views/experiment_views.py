from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from hyp.models import Experiment


@login_required
def index(request):
    if request.user.has_perm("hyp.view_experiment"):
        experiments = Experiment.objects.filter(
            customer_id=request.user.customer_id
        ).order_by('-created_at')

        return render(request, 'hyp/experiments/index.html', {"experiments": experiments})
    else:
        raise PermissionDenied


@login_required
def show(request, experiment_id):
    if request.user.has_perm("hyp.view_experiment"):
        experiment = get_object_or_404(
            Experiment, id=experiment_id, customer_id=request.user.customer_id
        )

        return render(request, 'hyp/experiments/show.html', {"experiment": experiment})
    else:
        raise PermissionDenied


@login_required
def create(request, params):
    if request.user.has_perm("hyp.read_experiment"):
        # TODO: want something like:
        # create experiment with request.POST['name']
        # interate over request.POST['variant_names'] and
        # create a variant for each, referncing the already
        # created experiment
        return HttpResponse("This is a no-op for now")
    else:
        raise PermissionDenied
