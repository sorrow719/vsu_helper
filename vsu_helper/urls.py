"""vsu_helper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from index import views as main_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', main_views.login_user),
    url(r'^logout/', main_views.logout_user),
    url(r'^registration/', main_views.registration),
    url(r'^result/', main_views.search_data),
    url(r'^description/', main_views.description),
    url(r'^support/', include('live_support.urls')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^get_select_data/', main_views.get_select_data),
    url(r'^$', main_views.index),
]
