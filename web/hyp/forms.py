from hyp.models import HypUser
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class HypUserChangeForm(UserChangeForm):

    class Meta:
        model = HypUser
        fields = ("username", "email")


class HypUserCreationForm(UserCreationForm):

    class Meta:
        model = HypUser
        fields = ("username", "email")
