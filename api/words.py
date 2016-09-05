#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from django.db.models import Sum
from django.utils.timesince import datetime
from core.models import Word, Occurence


class WordsList(APIView):

    def get(self, request, format=None):
        """
        Return a list of all words.
        """
        words = [{'name': word.name, 'id': word.id, 'weight': word.weight}
                 for word in Word.objects.all()
                 # .filter(rate__occurence__timestamp__date=datetime.datetime.today())
                 .annotate(weight=Sum('rate__weight')).order_by('-weight')[60:]]
        return Response(words)
