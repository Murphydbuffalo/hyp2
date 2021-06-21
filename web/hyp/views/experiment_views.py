from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
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
            "formset_errors": [],
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

        experiment = experiment_form.save(commit=False)
        experiment.customer_id = request.user.customer_id
        variant_formset = CreateVariantsFormset(request.POST, instance=experiment)
        context["variant_formset"] = variant_formset

        if experiment_form.is_valid() and variant_formset.is_valid():
            # TODO: redirect to show page for this experiment once that page is built out
            experiment = experiment_form.save()
            variants = variant_formset.save(commit=False)
            for variant in variants:
                variant.customer_id = experiment.customer_id
                variant.save()

            return redirect("/experiments/")
        else:
            context["formset_errors"] = variant_formset.non_form_errors()

            return render(request, 'hyp/experiments/new.html', context)
    else:
        raise PermissionDenied


@login_required
def update(request):
    if request.user.has_perm("hyp.change_experiment"):
        return HttpResponse("This is a no-op for now")
    else:
        raise PermissionDenied
