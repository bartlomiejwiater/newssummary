from core.models import Word, Rate, Occurence, Link
from django.utils.timezone import datetime, make_aware
import pytest


@pytest.mark.django_db
def test_ratemanager_creates_rate_object_connected_to_word():
    timestamp = make_aware(datetime(2015, 1, 1, 5, 30, 30))
    occurence = Occurence.objects.create(
        timestamp=timestamp, source='testsource')

    word = Word.objects.create(name='wow')
    Rate.objects.increase_or_create(word, occurence)

    assert Rate.objects.all().count() == 1
    assert Rate.objects.get(pk=1).weight == 1
    assert word.rate.all()[0] == Rate.objects.all()[0]


@pytest.mark.django_db
def test_ratemanager_mind_occurence_when_creating_rate_objects():
    word = Word.objects.create(name='word')

    timestamp_1 = make_aware(datetime(2015, 1, 1, 9, 30, 30))
    occurence_1 = Occurence.objects.create(
        timestamp=timestamp_1, source='testsource')
    Rate.objects.increase_or_create(word, occurence_1)

    timestamp_2 = make_aware(datetime(2015, 1, 5, 9, 30, 30))
    occurence_2 = Occurence.objects.create(
        timestamp=timestamp_2, source='testsource')
    Rate.objects.increase_or_create(word, occurence_2)

    assert Rate.objects.all().count() == 2


@pytest.mark.django_db
def test_ratemanager_increases_rate_when_item_and_occurence_the_same():
    timestamp = make_aware(datetime(2015, 1, 1, 5, 30, 30))
    occurence = Occurence.objects.create(
        timestamp=timestamp, source='testsource')

    word = Word.objects.create(name='word')
    Rate.objects.increase_or_create(word, occurence)
    Rate.objects.increase_or_create(word, occurence)

    assert Rate.objects.all().count() == 1
    assert Rate.objects.get(pk=1).weight == 2


@pytest.mark.django_db
def test_ratemanager_creates_rate_object_connected_to_link():
    link = Link.objects.create(
        title='wow', address='http://www.blabla.com/item/01/')

    timestamp = make_aware(datetime(2015, 1, 1, 5, 30, 30))
    occurence = Occurence.objects.create(
        timestamp=timestamp, source='testsource')
    Rate.objects.increase_or_create(link, occurence)

    assert Rate.objects.all().count() == 1
    assert Rate.objects.get(pk=1).weight == 1
