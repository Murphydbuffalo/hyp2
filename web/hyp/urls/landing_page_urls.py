from django.urls import path
from hyp.views import landing_page_views

urlpatterns = [
    path('', landing_page_views.index, name='home'),
]
