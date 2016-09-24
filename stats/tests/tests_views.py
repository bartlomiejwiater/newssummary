from django.urls import reverse
from django.test import TestCase, Client

from stats.views import words
from core.models import Word
from utils.factory import Factory


class TestWordsList(TestCase):
    url = reverse('stats-words-list')

    @classmethod
    def setUpClass(cls):
        super(TestWordsList, cls).setUpClass()
        f = Factory()
        cls.word1 = f.create_word_rate_occurence('test1', 'source1', rate=1)
        cls.word2 = f.create_word_rate_occurence('test2', 'source1', rate=2)

    def test_returns_200(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_uses_words_template(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'stats/words.html')

    def test_returns_word1_and_word2(self):
        response = self.client.get(self.url)

        self.assertContains(response, self.word1.name)
        self.assertContains(response, self.word2.name)

    def test_returns_error_msg_on_invalid_form(self):
        response = self.client.get('{0}?start_date=some'.format(self.url))
        self.assertContains(response,
                            '<div id="div_id_start_date" class="form-group has-error">')

    def test_returns_words_occured_only_in_range(self):
        f = Factory()
        from django.utils.timezone import datetime
        word3 = f.create_word_rate_occurence('test3', 'source1',
                                             dt=datetime(2015, 5, 5, 12))

        word4 = f.create_word_rate_occurence('test4', 'source1',
                                             dt=datetime(2015, 5, 8, 12))

        response = self.client.get(
            '{0}?start_date=2015-05-05&end_date=2015-05-06'.format(self.url))

        self.assertContains(response, word3.name)
        self.assertNotContains(response, word4.name)
