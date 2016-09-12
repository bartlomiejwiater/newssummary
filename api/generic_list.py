#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Sum
from django.utils.timesince import datetime
from core.models import Word, Link


class GenericList(APIView):

    list_class = ''

    def get(self, request, format=None):
        """
        Return a list of selected entry.
        """
        startdate, enddate = None, None
        source = None

        if 'startdate' in request.GET:
            startdate = request.GET['startdate']
        if 'enddate' in request.GET:
            enddate = request.GET['enddate']

        if self.list_class == Word:
            entries = self.list_class.objects.all().values('id', 'name')
        elif self.list_class == Link:
            entries = self.list_class.objects.all().values('id', 'title', 'address')

        if 'words' in request.GET and self.list_class == Link:
            wanted_words = request.GET.getlist('words')
            entries = self.fiter_links_according_to_word(entries, wanted_words)

        if startdate and enddate:
            entries = entries.filter(
                rate__occurence__timestamp__date__range=(startdate, enddate))
        elif startdate and enddate is None:
            entries = entries.filter(
                rate__occurence__timestamp__date__gte=startdate)
        elif startdate is None and enddate:
            entries = entries.filter(
                rate__occurence__timestamp__date__lte=enddate)

        if 'source' in request.GET:
            source = request.GET.getlist('source')
            entries = entries.filter(rate__occurence__source__in=source)

        entries = entries.annotate(
            weight=Sum('rate__weight')).order_by('-weight')[:60]

        results = {'results': entries}
        return Response(results)

    def fiter_links_according_to_word(self, wanted_words):
        raise NotImplementedError
