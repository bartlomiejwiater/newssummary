#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from api.urls import urlpatterns as api_urlspatter

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('api.urls')),
]
