from hyp.models import Experiment, HypUser, Variant
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import modelform_factory, inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError

class HypUserChangeForm(UserChangeForm):
    class Meta:
        model = HypUser
        fields = ("username", "email")


class HypUserCreationForm(UserCreationForm):
    class Meta:
        model = HypUser
        fields = ("username", "email")


ExperimentForm = modelform_factory(Experiment, fields=["name"])
class BaseVariantFormSet(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        names = []
        for form in self.forms:
            name = form.cleaned_data.get('name')
            if name in name:
                raise ValidationError("Each variant must have a unique name.")
            name.append(name)

CreateVariantsFormset = inlineformset_factory(
    Experiment,
    Variant,
    fields=["name"],
    can_delete=False,
    min_num=2,
    max_num=10,
    validate_min=True,
    extra=0,
    formset=BaseVariantFormSet,
)
