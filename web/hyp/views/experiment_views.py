from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from hyp.models import Experiment, Variant


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
def new(request):
    if request.user.has_perm("hyp.add_experiment"):
        return render(request, 'hyp/experiments/new.html')
    else:
        raise PermissionDenied


@login_required
def create(request, params):
    if request.user.has_perm("hyp.add_experiment"):
        # TODO: how to do a transaction?
        experiment = Experiment(customer=request.user.customer, name=request.POST["name"])
        experiment.save()
        for variant_name in request.POST["variant_names"]:
            variant = Variant(
                experiment=experiment,
                customer=request.customer,
                name=variant_name
            )
            variant.save()

        return redirect("/experiments/")
    else:
        raise PermissionDenied


@login_required
def update(request, params):
    if request.user.has_perm("hyp.change_experiment"):
        return HttpResponse("This is a no-op for now")
    else:
        raise PermissionDenied
