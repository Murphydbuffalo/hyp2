from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('experiments', views.index, name='index'),
    path('experiments/<int:experiment_id>/', views.show, name='show'),
    path('variant_assignment/<str:participant_id>/<int:experiment_id>/', views.variant_assignment, name='variant_assignment'),
    path('record_conversion/<str:participant_id>/<int:experiment_id>/', views.variant_assignment, name='record_conversion'),
]
