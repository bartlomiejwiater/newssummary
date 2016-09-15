#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from api.words import WordsList
from api.links import LinksList
from api.select_words import SelectWords

urlpatterns = [
    url(r'^words/', WordsList.as_view(), name='words-list'),
    url(r'^links/', LinksList.as_view(), name='links-list'),
    url(r'^select_words/', SelectWords.as_view(), name='words-select'),
]
