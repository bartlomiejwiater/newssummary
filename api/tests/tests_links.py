#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from django.utils.timezone import datetime, make_aware

from core.models import Link, Occurence, Rate


class Factory:

    def create_link_rate_occurence(self, title, address, source, dt, rate=1):
        link, created = Link.objects.get_or_create(
            title=title, address=address)
        timestamp = make_aware(dt)
        occurence, created = Occurence.objects.get_or_create(
            timestamp=timestamp, source=source)

        for x in range(rate):
            Rate.objects.increase_or_create(link, occurence)


class TestWordsList(APITestCase, Factory):

    @classmethod
    def setUpClass(cls):
        super(TestWordsList, cls).setUpClass()

        cls.create_link_rate_occurence(
            cls, 'test_title', 'http://www.test_address.com', 'testsource', datetime.now())

    def test_get(self):
        url = reverse('links-list')
        response = self.client.get(url, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK

    def test_post(self):
        url = reverse('links-list')
        response = self.client.post(url, content_type='application/json')

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
