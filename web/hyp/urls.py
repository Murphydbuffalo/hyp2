from django.urls import path

from hyp.views import landing_page_views
from hyp.views import api_views

# TODO: look into django REST framework
# might save us a lot of work with authorization, building the API?
# https://www.django-rest-framework.org/
urlpatterns = [
    path('', landing_page_views.index, name='index'),
    path('experiments', landing_page_views.index, name='index'),
    path('experiments/<int:experiment_id>/', landing_page_views.show, name='show'),
    # TODO: URL namespace for api/v1
    # TODO: maybe use re_path to have a regex handle the trailing slash?
    # Would Django REST framework take care of this for us?
    path('assign/<str:participant_id>/<int:experiment_id>', api_views.variant_assignment, name='variant_assignment'),
    path('convert/<str:participant_id>/<int:experiment_id>', api_views.conversion, name='conversion'),
    path('assign/<str:participant_id>/<int:experiment_id>/', api_views.variant_assignment, name='variant_assignment'),
    path('convert/<str:participant_id>/<int:experiment_id>/', api_views.conversion, name='conversion'),
]
