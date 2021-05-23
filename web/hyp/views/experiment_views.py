# TODO: in all our views, render errors if validation fails
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from hyp.models import Experiment, Variant
from hyp.forms import ExperimentForm, VariantForm


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
        return render(request, 'hyp/experiments/new.html', {"num_optional_variants": range(2, 5)})
    else:
        raise PermissionDenied


@login_required
@transaction.atomic
def create(request):
    if request.user.has_perm("hyp.add_experiment"):
        context = { "errors": [] }
        experiment_form = ExperimentForm({
            "customer": request.user.customer,
            "name": request.POST["experiment-name"]
        })

        if experiment_form.is_valid():
            experiment = experiment_form.save()
        else:
            context["errors"].append(experiment_form.errors)

        variants = []
        variant_names = [request.POST[f'variant-{i}-name'] for i in range(0,5)]
        variant_names = [n for n in variant_names if not n is None or len(n) == 0]

        if len(variant_names) < 2:
            context["errors"].append({ "num_variants": "Must have at least 2 variants for every experiment." })
        else:
            for i, name in enumerate(variant_names):
                variant_form = VariantForm({
                    "name": name,
                    "experiment": experiment,
                    "customer": experiment.customer,
                    "baseline": (i==0)
                })

                if variant_form.is_valid():
                    variant = variant_form.save()
                    variants.append(variant)
                else:
                    context["errors"].append(variant_form.errors)

        return redirect("/experiments/", context)
    else:
        raise PermissionDenied


@login_required
def update(request):
    if request.user.has_perm("hyp.change_experiment"):
        return HttpResponse("This is a no-op for now")
    else:
        raise PermissionDenied
