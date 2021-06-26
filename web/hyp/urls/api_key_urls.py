from django.urls import path
from hyp.views import api_key_views

urlpatterns = [
    path('', api_key_views.index, name='api_keys'),
    path('new/', api_key_views.new, name='new_api_key'),
    path('create/', api_key_views.create, name='create_api_key'),
    path('deactivate/<int:api_key_id>/', api_key_views.deactivate, name='deactivate_api_key'),

]
