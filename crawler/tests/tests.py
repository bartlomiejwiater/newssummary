from django.test import TestCase
from crawler.items_saver import ItemSaver
from core.models import Link, Occurence, Word
from django.utils.timezone import datetime, make_aware


class TestItemSaver(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestItemSaver, cls).setUpClass()

        cls.source = 'BLABLA'
        cls.timestamp = make_aware(datetime(2015, 1, 1, 5, 30, 30))
        cls.title = 'Item 01 example word na to'

        itemsaver = ItemSaver(cls.source, cls.timestamp)
        itemsaver.save_link_and_words(
            'http://www.blabla.com/item/01/', cls.title)

    def test_itemsaver_creates_occurence(self):
        self.assertEqual(1, Occurence.objects.all().count())
        self.assertEqual(self.source, Occurence.objects.first().source)
        self.assertEqual(self.timestamp, Occurence.objects.first().timestamp)

    def test_itemsaver_creates_link(self):
        self.assertEqual(1, Link.objects.all().count())
        self.assertEqual(self.title, Link.objects.first().title)
        self.assertEqual('http://www.blabla.com/item/01/',
                         Link.objects.first().address)

    def test_itemsaver_creates_words(self):
        words = self.title.split(' ')
        self.assertEqual(1, len(Word.objects.filter(name=words[0])))
        self.assertEqual(1, len(Word.objects.filter(name=words[1])))
        self.assertEqual(1, len(Word.objects.filter(name=words[2])))
        self.assertEqual(1, len(Word.objects.filter(name=words[3])))

    def test_itemsaver_cleans_words_in_title(self):
        self.fail('Write me!')

    def test_itemsaver_creates_rate_for_each_item(self):
        self.fail('Write me!')

    def test_itemsaver_connects_words_and_link(self):
        self.assertEqual(4, Link.objects.first().words.count())


class Test(TestCase):

    @classmethod
    def setUpClass(cls):
        super(Test, cls).setUpClass()

        cls.source = 'BLABLA'
        cls.timestamp = make_aware(datetime(2015, 1, 1, 5, 30, 30))
        cls.title = 'Gol, gol, gol'

        itemsaver = ItemSaver(cls.source, cls.timestamp)
        itemsaver.save_link_and_words(
            'http://www.blabla.com/item/01/', cls.title)

    def test_cs_mind_case(self):
        self.assertEqual(2, Word.objects.all().count())
