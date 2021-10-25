from django.urls import path
from hyp.views import account_views

urlpatterns = [
    path('settings/', account_views.show, name='settings'),
]
