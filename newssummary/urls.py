#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from api.urls import urlpatterns as api_urlspatter

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('api.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
