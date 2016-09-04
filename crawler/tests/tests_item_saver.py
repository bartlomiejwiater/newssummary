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
        cls.title = 'Za wcześnie na powrót Pana X'

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
        self.assertEqual(0, len(Word.objects.filter(name=words[0])))
        self.assertEqual(1, len(Word.objects.filter(name=words[1])))
        self.assertEqual(0, len(Word.objects.filter(name=words[2])))
        self.assertEqual(1, len(Word.objects.filter(name=words[3])))
        self.assertEqual(1, len(Word.objects.filter(name=words[4])))
        self.assertEqual(1, len(Word.objects.filter(name=words[5])))

    def test_itemsaver_cleans_words_in_title(self):
        with self.assertRaises(Word.DoesNotExist):
            Word.objects.get(name='Za')

    def test_itemsaver_connects_words_and_link(self):
        self.assertEqual(4, Link.objects.first().words.count())

    def test_itemsaver_creates_rank_for_word(self):
        word = Word.objects.get(name='wcześnie')
        assert word.rate.all().count() == 1

    def test_itemsaver_creates_rank_for_link(self):
        link = Link.objects.get(address='http://www.blabla.com/item/01/')
        assert link.rate.all().count() == 1


class TestItemSaver_MindCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestItemSaver_MindCase, cls).setUpClass()

        itemsaver = ItemSaver('source', make_aware(datetime.now()))
        itemsaver.save_link_and_words(
            'http://www.blabla.com/item/01/', 'Gol, gol, gol')

    def test_itemsaver_mind_case(self):
        self.assertEqual(2, Word.objects.all().count())
