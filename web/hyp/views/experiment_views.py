from django.http import HttpResponse
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from hyp.models import Experiment, Variant
from hyp.forms import ExperimentForm, CreateVariantsFormset


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
        experiment = Experiment()
        context = {
            "experiment_form": ExperimentForm(instance=experiment),
            "variant_formset": CreateVariantsFormset(instance=experiment),
        }
        return render(request, 'hyp/experiments/new.html', context)
    else:
        raise PermissionDenied


@login_required
@transaction.atomic
def create(request):
    if request.user.has_perm("hyp.add_experiment"):
        experiment_form = ExperimentForm(request.POST)
        context = { "experiment_form": experiment_form }

        experiment = Experiment()
        if experiment_form.is_valid():
            experiment = experiment_form.save(commit=False)

        experiment.customer_id = request.user.customer_id
        variant_formset = CreateVariantsFormset(request.POST, instance=experiment)
        context["variant_formset"] = variant_formset

        if experiment_form.is_valid() and variant_formset.is_valid():
            try:
                experiment.validate_unique()
                experiment = experiment_form.save()
                variants = variant_formset.save(commit=False)
                for variant in variants:
                    variant.customer_id = experiment.customer_id
                    variant.save()

                return redirect(f'/experiments/{experiment.id}/')
            except(ValidationError):
              context["unique_error"] = "Experiment name is already taken."
              return render(request, 'hyp/experiments/new.html', context)
        else:
            return render(request, 'hyp/experiments/new.html', context)
    else:
        raise PermissionDenied


@login_required
def update(request):
    if request.user.has_perm("hyp.change_experiment"):
        # TODO: should be able to update the name of an experiment at any time
        # TOOD: should be able to update variant names at any time
        # TODO: should be able to stop/restart an experiment at any time, but we probably 
        # want to do that as a separate ticket as it necessitates skipping the Thompson
        # sampler and instead always directing users to the best performing variant.
        return HttpResponse("This is a no-op for now")
    else:
        raise PermissionDenied


@login_required
def destroy(request):
    if request.user.has_perm("hyp.change_experiment"):
        # TODO: should be able to destroy an experiment if it hasn't started
        # otherwise, they can pause it and filter it out of the view that way.
        return HttpResponse("This is a no-op for now")
    else:
        raise PermissionDenied
