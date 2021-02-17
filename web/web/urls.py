"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import debug_toolbar

handler404 = 'hyp.views.shared_views.handler404'
handler500 = 'hyp.views.shared_views.handler500'

urlpatterns = [
    path('', include('hyp.urls.landing_page_urls')),
    path('experiments/', include('hyp.urls.experiment_urls')),
    path('api/v1/', include('hyp.urls.api_urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('hyp.urls.account_urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]
