from django.urls import path
from hyp.views import api_views

urlpatterns = [
    path(
        'assign/<str:participant_id>/<int:experiment_id>',
        api_views.variant_assignment, name='assign'
    ),
    path(
        'convert/<str:participant_id>/<int:experiment_id>',
        api_views.record_conversion, name='convert'
    ),

    # Handle optional trailing slash without needing to redirect or write a
    # regexp that duplicates the built in matchers like `<str:participant_id>`
    # By default Django will 301 (permanent) redirect to the correct route if a
    # trailing slash is left out. But we can't rely on that for API requests
    # and don't want to incur the performance overhead either.
    path(
        'assign/<str:participant_id>/<int:experiment_id>/',
        api_views.variant_assignment, name='assign'
    ),
    path(
        'convert/<str:participant_id>/<int:experiment_id>/',
        api_views.record_conversion, name='convert'
    ),
]
