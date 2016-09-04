#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from core.models import Word, Occurence


class WordResource(ModelResource):

    class Meta:
        queryset = Word.objects.all()
        resource_name = 'words'
