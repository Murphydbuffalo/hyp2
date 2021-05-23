from hyp.models import Experiment, HypUser, Variant
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import modelform_factory

class HypUserChangeForm(UserChangeForm):
    class Meta:
        model = HypUser
        fields = ("username", "email")


class HypUserCreationForm(UserCreationForm):
    class Meta:
        model = HypUser
        fields = ("username", "email")


ExperimentForm = modelform_factory(Experiment, fields=["name", "customer"])
VariantForm = modelform_factory(Variant, fields=["name", "baseline", "customer", "experiment"])
