#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Sum
from core.models import Word, Link


class GenericList(APIView):

    list_class = ''

    def get(self, request, format=None):
        """
        Return a list of selected entry.
        """
        filter_kwargs = {}

        if 'startdate' in request.GET:
            filter_kwargs['startdate'] = request.GET['startdate']
        if 'enddate' in request.GET:
            filter_kwargs['enddate'] = request.GET['enddate']
        if 'source' in request.GET:
            filter_kwargs['source'] = request.GET.getlist('source')

        if self.list_class == Word:
            entries = self.list_class.objects.all().values('id', 'name')
        elif self.list_class == Link:
            entries = self.list_class.objects.all().values('id', 'title', 'address')
        else:
            raise NotImplementedError

        if 'words' in request.GET and self.list_class == Link:
            wanted_words = request.GET.getlist('words')
            entries = self.fiter_links_according_to_word(entries, wanted_words)
        elif 'words' in request.GET and self.list_class == Word:
            # TODO: Write tests
            wanted_words = request.GET.getlist('words')
            print(wanted_words)
            entries = entries.filter(name__in=wanted_words)

        entries = self.filter(entries, **filter_kwargs)
        entries = entries.annotate(
            weight=Sum('rate__weight')).order_by('-weight')[:60]
        results = {'results': entries}

        return Response(results)

    def filter(self, queryset, **kwargs):
        startdate = kwargs.get('startdate', None)
        enddate = kwargs.get('enddate', None)

        if startdate and enddate:
            queryset = queryset.filter(
                rate__occurence__timestamp__date__range=(startdate, enddate))
        elif startdate and enddate is None:
            queryset = queryset.filter(
                rate__occurence__timestamp__date__gte=startdate)
        elif startdate is None and enddate:
            queryset = queryset.filter(
                rate__occurence__timestamp__date__lte=enddate)

        source = kwargs.get('source', None)

        if source:
            queryset = queryset.filter(rate__occurence__source__in=source)

        return queryset

    def fiter_links_according_to_word(self, wanted_words):
        raise NotImplementedError
