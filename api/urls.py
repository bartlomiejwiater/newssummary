#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from api.words import WordsList

urlpatterns = [
    url(r'^api/words/', WordsList.as_view(), name='words-list')
]
