from django.urls import path

from hyp.views import landing_page_views
from hyp.views import api_views

urlpatterns = [
    path('', landing_page_views.index, name='index'),
    path('experiments', landing_page_views.index, name='index'),
    path('experiments/<int:experiment_id>/', landing_page_views.show, name='show'),
    path('api/v1/assign/<str:participant_id>/<int:experiment_id>', api_views.variant_assignment, name='assign'),
    path('api/v1/convert/<str:participant_id>/<int:experiment_id>', api_views.record_conversion, name='convert'),
]
