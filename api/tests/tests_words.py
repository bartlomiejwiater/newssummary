#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from datetime import date
from django.utils.timezone import datetime, make_aware
from furl import furl

from core.models import Word, Rate, Occurence


class Factory:

    def create_word_rate_occurence(self,  name, source, dt, rate=1):
        word, created = Word.objects.get_or_create(name=name)
        timestamp = make_aware(dt)
        occurence, created = Occurence.objects.get_or_create(
            timestamp=timestamp, source=source)

        for x in range(rate):
            Rate.objects.increase_or_create(word, occurence)

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


class TestWordsList(APITestCase, Factory):

    @classmethod
    def setUpClass(cls):
        super(TestWordsList, cls).setUpClass()

        cls.create_word_rate_occurence(
            cls, 'test_word', 'testsource', datetime.now())

    def test_returns_results_list(self):
        url = reverse('words-list')
        response = self.client.get(url, content_type='application/json')

        assert 'results' in response.data

    def test_returns_words_inside_results_list_have_keys_and_values(self):
        url = reverse('words-list')
        response = self.client.get(url, content_type='application/json')

        word_0 = response.data['results'][0]
        assert 'name' in word_0
        assert 'test_word' == word_0['name']

        assert 'id' in word_0
        assert 1 == word_0['id']

        assert 'weight' in word_0
        assert 1 == word_0['weight']


class TestWordsListDateFilteringAndSorting(APITestCase, Factory):

    @classmethod
    def setUpClass(cls):
        super(TestWordsListDateFilteringAndSorting, cls).setUpClass()

        cls.create_word_rate_occurence(
            cls, 'test_word1', 'testsource', datetime(2015, 3, 3, 12))
        cls.create_word_rate_occurence(
            cls, 'test_word1', 'testsource', datetime(2015, 3, 5, 12))
        cls.create_word_rate_occurence(
            cls, 'test_word1', 'testsource', datetime(2015, 3, 6, 12))
        cls.create_word_rate_occurence(
            cls, 'test_word2', 'testsource', datetime(2015, 3, 7, 12), 2)
        cls.create_word_rate_occurence(
            cls, 'test_word3', 'testsource', datetime(2015, 3, 8, 12), 2)

    def test_returns_words_and_weight_occured_before_enddate(self):
        url = furl(reverse('words-list')).add({'enddate': '2015-03-05'}).url
        response = self.client.get(url, content_type='application/json')

        assert 1 == len(self.get_results(response))
        assert 2 == self.get_weight(response, 0)

    def test_returns_words_and_weight_occured_after_startdate(self):
        url = furl(reverse('words-list')).add({'startdate': '2015-03-06'}).url
        response = self.client.get(url, content_type='application/json')

        assert 3 == len(response.data['results'])

        names = self.get_names(response)

        assert 'test_word2' in names
        assert 2 == self.get_weight(response, 'test_word2')

        assert 'test_word3' in names
        assert 2 == self.get_weight(response, 'test_word3')

        assert 'test_word1' in names
        assert 1 == self.get_weight(response, 'test_word1')

    def test_returns_words_and_weight_occured_between_startdate_and_enddate(self):
        kwargs = {'startdate': '2015-03-05', 'enddate': '2015-03-07'}
        url = furl(reverse('words-list')).add(kwargs).url
        response = self.client.get(url, content_type='application/json')

        names = self.get_names(response)

        assert 2 == len(self.get_results(response))

        assert 'test_word1' in names
        assert 2 == self.get_weight(response, 'test_word1')

        assert 'test_word2' in names
        assert 2 == self.get_weight(response, 'test_word2')

        assert 'test_word3' not in names

    def test_returns_words_sorted_according_to_weight_desc(self):
        url = reverse('words-list')
        response = self.client.get(url, content_type='application/json')

        assert self.get_weight(response, 0) >= self.get_weight(response, 1)


class TestWordsListSourceFiltering(APITestCase, Factory):

    @classmethod
    def setUpClass(cls):
        super(TestWordsListSourceFiltering, cls).setUpClass()

        cls.create_word_rate_occurence(
            cls, 'test_word1', 'test.source1', datetime(2015, 3, 3, 12))

        cls.create_word_rate_occurence(
            cls, 'test_word1', 'testsource2', datetime(2015, 3, 4, 12))

        cls.create_word_rate_occurence(
            cls, 'test_word2', 'testsource2', datetime(2015, 3, 5, 12))

        cls.create_word_rate_occurence(
            cls, 'test_word3', 'testsource3', datetime(2015, 3, 6, 12))

    def test_returns_words_only_from_source(self):
        kwargs = {'source': 'test.source1'}
        url = furl(reverse('words-list')).add(kwargs).url
        response = self.client.get(url, content_type='application/json')

        names = self.get_names(response)

        assert 'test_word1' in names
        assert 'test_word2' not in names
        assert 'test_word3' not in names

    def test_returns_words_weight_only_from_source(self):
        kwargs = {'source': 'test.source1'}
        url = furl(reverse('words-list')).add(kwargs).url
        response = self.client.get(url, content_type='application/json')

        names = self.get_names(response)

        assert 1 == self.get_weight(response, 'test_word1')

    def test_returns_words_only_from_many_sources(self):
        kwargs = {'source': ['test.source1', 'testsource2']}
        url = furl(reverse('words-list')).add(kwargs).url
        print(url)
        response = self.client.get(url, content_type='application/json')

        names = self.get_names(response)

        assert 'test_word1' in names
        assert 2 == self.get_weight(response, 'test_word1')

        assert 'test_word2' in names
        assert 1 == self.get_weight(response, 'test_word2')

        assert 'test_word3' not in names
