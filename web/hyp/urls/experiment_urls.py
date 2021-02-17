from django.urls import path
from hyp.views import experiment_views

urlpatterns = [
    path('', experiment_views.index, name='experiments'),
    path('<int:experiment_id>/', experiment_views.show, name='experiment'),
]
