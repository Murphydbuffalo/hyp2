from django.urls import path
from hyp.views import api_key_views

urlpatterns = [
    path('', api_key_views.index, name='api_keys'),
    path('rotate', api_key_views.rotate, name='rotate_api_key'),
]
