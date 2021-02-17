from django.urls import path
from hyp.views import account_views

urlpatterns = [
    path('profile/', account_views.show, name='profile'),
]
