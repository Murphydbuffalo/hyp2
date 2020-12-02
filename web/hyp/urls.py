from django.urls import path

from . import views

# TODO: look into django REST framework
# might save us a lot of work with authorization, building the API?
# https://www.django-rest-framework.org/
urlpatterns = [
    path('', views.index, name='index'),
    path('experiments', views.index, name='index'),
    path('experiments/<int:experiment_id>/', views.show, name='show'),
    # TODO: URL namespace for api/v1
    # TODO: maybe use re_path to have a regex handle the trailing slash?
    # Would Django REST framework take care of this for us?
    path('assign/<str:participant_id>/<int:experiment_id>', views.variant_assignment, name='variant_assignment'),
    path('convert/<str:participant_id>/<int:experiment_id>', views.conversion, name='conversion'),
    path('assign/<str:participant_id>/<int:experiment_id>/', views.variant_assignment, name='variant_assignment'),
    path('convert/<str:participant_id>/<int:experiment_id>/', views.conversion, name='conversion'),
]
