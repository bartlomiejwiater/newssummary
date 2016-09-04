#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tastypie.api import Api
from django.conf.urls import url, include
from api.words import WordResource


v1_api = Api(api_name='v1')
v1_api.register(WordResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls))
]
