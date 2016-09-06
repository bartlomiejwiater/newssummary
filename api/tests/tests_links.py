#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from django.utils.timezone import datetime
from furl import furl

from api.tests.factory import Factory


class TestWordsList(APITestCase, Factory):

    @classmethod
    def setUpClass(cls):
        super(TestWordsList, cls).setUpClass()

        cls.create_link_rate_occurence(
            cls, 'test_title', 'http://www.test_address.com',
            'testsource', datetime.now())

    def test_get(self):
        url = reverse('links-list')
        response = self.client.get(url, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK

    def test_post(self):
        url = reverse('links-list')
        response = self.client.post(url, content_type='application/json')

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_returns_results_list(self):
        url = reverse('links-list')
        response = self.client.get(url, content_type='application/json')

        assert 'results' in response.data

    def test_returns_words_inside_results_list_have_keys_and_values(self):
        url = reverse('links-list')
        response = self.client.get(url, content_type='application/json')

        word_0 = response.data['results'][0]
        assert 'title' in word_0
        assert 'test_title' == word_0['title']

        assert 'id' in word_0
        assert 1 == word_0['id']

        assert 'address' in word_0
        assert 'http://www.test_address.com' == word_0['address']

        assert 'weight' in word_0
        assert 1 == word_0['weight']


class TestLinksListFilterByWordName(APITestCase, Factory):

    def setUp(self):
        title1 = 'The lack of competition'
        self.create_link_word_rate_occurence(title1.split(
            ' '), title1, 'http://www.test.org/title1/', 'testsource', datetime.now())

        title2 = 'Is The World Becoming Safer'
        self.create_link_word_rate_occurence(title2.split(
            ' '), title2, 'http://www.test.org/title2/', 'testsource', datetime.now())

    def test_returns_link_connected_to_word(self):
        kwargs = {'word': 'The'}
        url = furl(reverse('links-list')).add(kwargs).url
        response = self.client.get(url, content_type='application/json')

        titles = self.get_titles(response)

        assert 2 == len(self.get_results(response))
        assert 'The lack of competition' in titles
        assert 'Is The World Becoming Safer' in titles

    def test__does_not_return_link_connected_to_word(self):
        kwargs = {'words': 'World'}
        url = furl(reverse('links-list')).add(kwargs).url
        response = self.client.get(url, content_type='application/json')

        titles = self.get_titles(response)

        assert 1 == len(self.get_results(response))
        assert 'The lack of competition' not in titles
        assert 'Is The World Becoming Safer' in titles
