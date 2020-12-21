from django.contrib import admin

from hyp.models import ApiKey, Customer, Experiment, Interaction, Variant

admin.site.register(Customer)
admin.site.register(ApiKey)
admin.site.register(Experiment)
admin.site.register(Variant)
admin.site.register(Interaction)
