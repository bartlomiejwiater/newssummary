#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.models import Word, Rate, Occurence, Link
from django.utils.timezone import datetime, make_aware


class Factory(object):

    def create_word_rate_occurence(self, name, source, dt=datetime.now(), rate=1):
        word, created = Word.objects.get_or_create(name=name)

        timestamp = make_aware(dt)
        occurence, created = Occurence.objects.get_or_create(
            timestamp=timestamp, source=source)

        for x in range(rate):
            Rate.objects.increase_or_create(word, occurence)

        return word

    def create_link_rate_occurence(self, title, address, source, dt=datetime.now(), rate=1):
        link, created = Link.objects.get_or_create(
            title=title, address=address)
        timestamp = make_aware(dt)
        occurence, created = Occurence.objects.get_or_create(
            timestamp=timestamp, source=source)

        for x in range(rate):
            Rate.objects.increase_or_create(link, occurence)

        return link

    def create_link_word_rate_occurence(self, names, title, address, source, dt, rate=1):
        words = []
        for name in names:
            word_obj = self.create_word_rate_occurence(
                name=name, source=source, dt=dt, rate=rate)
            words.append(word_obj)

        link = self.create_link_rate_occurence(
            title, address, sorted, dt, rate)

        link.words.add(*words)

        link.save()

    def get_results(self, response):
        return response.data['results']

    def get_weight(self, response, item):
        if isinstance(item, int):
            return self.get_results(response)[item]['weight']
        else:
            for word in self.get_results(response):
                if word['name'] == item:
                    return word['weight']

    def get_names(self, response):
        return [x['name'] for x in response.data['results']]

    def get_titles(self, response):
        return [x['title'] for x in response.data['results']]
