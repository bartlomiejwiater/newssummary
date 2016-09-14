from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /stats/
    url(r'^words/', views.words, name='stats-words-list'),
]
