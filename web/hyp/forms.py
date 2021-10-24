from hyp.models import Experiment, HypUser, Variant
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm, TextInput, inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError


class HypUserChangeForm(UserChangeForm):
    class Meta:
        model = HypUser
        fields = ("username", "email")


class HypUserCreationForm(UserCreationForm):
    class Meta:
        model = HypUser
        fields = ("username", "email")


class ExperimentForm(ModelForm):
    class Meta:
        model = Experiment
        fields = ("name",)
        widgets = {
            "name": TextInput(attrs={"placeholder": "Experiment name"})
        }


class BaseVariantFormSet(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        names = []
        for form in self.forms:
            name = form.cleaned_data.get("name")
            if name in names:
                raise ValidationError("Each variant must have a unique name.")
            names.append(name)

        if sum(name is not None and len(name) > 0 for name in names) < 2:
            raise ValidationError("An experiment must have at least 2 variants.")


CreateVariantsFormset = inlineformset_factory(
    Experiment,
    Variant,
    fields=["name"],
    widgets={"name": TextInput(attrs={"placeholder": "Variant name"})},
    can_delete=False,
    min_num=2,
    max_num=5,
    extra=0,
    formset=BaseVariantFormSet,
)
