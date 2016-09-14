from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /stats/
    url(r'^', views.temp, name='index'),
]
