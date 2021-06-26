from django.urls import path
from hyp.views import experiment_views

urlpatterns = [
    path('', experiment_views.index, name='experiments'),
    path('<int:experiment_id>/', experiment_views.show, name='experiment'),
    path('new/', experiment_views.new, name='new_experiment'),
    path('create/', experiment_views.create, name='create_experiment'),
    path('update/', experiment_views.update, name='update_experiment'),
    path('destroy/', experiment_views.destroy, name='destroy_experiment'),
]
