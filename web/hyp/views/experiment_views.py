from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from hyp.models import Experiment, Variant
from hyp.forms import ExperimentForm, VariantForm


MAX_NUM_VARIANTS = 5
NUM_REQUIRED_VARIANTS = 2

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
        context = {
            "num_optional_variants": range(NUM_REQUIRED_VARIANTS, MAX_NUM_VARIANTS),
            "errors": [],
        }
        return render(request, 'hyp/experiments/new.html', context)
    else:
        raise PermissionDenied


@login_required
@transaction.atomic
def create(request):
    if request.user.has_perm("hyp.add_experiment"):
        experiment_form = ExperimentForm({
            "customer": request.user.customer,
            "name": request.POST["experiment-name"]
        })
        experiment = Experiment()

        if experiment_form.is_valid():
            experiment = experiment_form.save(commit=False)

        variant_names = [request.POST[f'variant-{i}-name'] for i in range(MAX_NUM_VARIANTS)]
        valid_variant_forms = []
        invalid_variant_forms = []
        for i, name in enumerate(variant_names):
            variant_form = VariantForm({
                "name": name,
                "experiment": experiment,
                "customer": request.user.customer,
                "baseline": (i==0)
            })

            if variant_form.is_valid():
                valid_variant_forms.append(variant_form)
            else:
                invalid_variant_forms.append(variant_form)

        if experiment_form.is_valid() and len(valid_variant_forms) >= 2:
            experiment.save()
            for variant_form in valid_variant_forms:
                variant_form.save()

            return redirect("/experiments/")
        else:
            context = {
                "num_optional_variants": range(NUM_REQUIRED_VARIANTS, MAX_NUM_VARIANTS),
                "errors": ["Must provide a unique name for the experiment and at least 2 variants."],
            }

            return render(request, 'hyp/experiments/new.html', context)


    else:
        raise PermissionDenied


@login_required
def update(request):
    if request.user.has_perm("hyp.change_experiment"):
        return HttpResponse("This is a no-op for now")
    else:
        raise PermissionDenied
