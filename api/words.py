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
        startdate, enddate = None, None
        source = None

        if 'startdate' in request.GET:
            startdate = request.GET['startdate']
        if 'enddate' in request.GET:
            enddate = request.GET['enddate']

        words = Word.objects.all().values('id', 'name')

        if startdate and enddate:
            words = words.filter(
                rate__occurence__timestamp__date__range=(startdate, enddate))
        elif startdate and enddate is None:
            words = words.filter(
                rate__occurence__timestamp__date__gte=startdate)
        elif startdate is None and enddate:
            words = words.filter(rate__occurence__timestamp__date__lte=enddate)

        if 'source' in request.GET:
            source = request.GET.getlist('source')
            words = words.filter(rate__occurence__source__in=source)

        words = words.annotate(
            weight=Sum('rate__weight')).order_by('-weight')[:60]

        results = {'results': words}
        return Response(results)
