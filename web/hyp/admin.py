from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from hyp.forms import HypUserCreationForm, HypUserChangeForm
from hyp.models import ApiKey, Customer, Experiment, Interaction, Variant, HypUser


class HypUserAdmin(UserAdmin):
    add_form = HypUserCreationForm
    form = HypUserChangeForm
    model = HypUser
    list_display = ['email']


admin.site.register(Customer)
admin.site.register(ApiKey)
admin.site.register(Experiment)
admin.site.register(Variant)
admin.site.register(Interaction)
admin.site.register(HypUser, HypUserAdmin)
