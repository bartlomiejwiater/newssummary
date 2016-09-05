#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from datetime import date
from django.utils.timezone import datetime, make_aware

from core.models import Word, Rate, Occurence


class TestWordsList(APITestCase):

    def setUp(self):
        word = Word.objects.create(name='test_word')

        timestamp = make_aware(datetime.now())
        occurence = Occurence.objects.create(
            timestamp=timestamp, source='testsource')

        Rate.objects.increase_or_create(word, occurence)

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
