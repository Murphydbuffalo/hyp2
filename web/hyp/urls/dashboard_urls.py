from django.urls import path
from hyp.views import dashboard_views

urlpatterns = [
    path('', dashboard_views.index, name='index'),
    path('experiments/', dashboard_views.index, name='index'),
    path('experiments/<int:experiment_id>/', dashboard_views.show, name='show'),
]
