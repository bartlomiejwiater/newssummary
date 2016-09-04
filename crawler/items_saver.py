#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crawler.title_cleaner import TitleCleaner
from core.models import Occurence, Link, Word, Rate


class ItemSaver:

    def __init__(self, source, timestamp):
        self.source = source
        self.timestamp = timestamp
        self.occurence = None

    def save_link_and_words(self, address, title):

        if not title.strip():
            return

        if not self.occurence:
            self.get_or_create_occurence()

        clean_title = self.clean_title(title)
        word_objects = self.save_words(clean_title)
        link = self.save_link(address, title, word_objects)
        self.connect_words_and_link(word_objects, link)

    def get_or_create_occurence(self):
        self.occurence, created = Occurence.objects.get_or_create(
            timestamp=self.timestamp, source=self.source)

    def clean_title(self, title):
        clean_title = TitleCleaner(title).clean()
        return clean_title

    def save_words(self, clean_title):
        word_objects = []
        for word in clean_title.split(' '):
            word_object, created = Word.objects.get_or_create(name=word)
            word_objects.append(word_object)
            Rate.objects.increase_or_create(word_object, self.occurence)
        return word_objects

    def save_link(self, address, title, words_to_connect):
        link, o = Link.objects.get_or_create(address=address, title=title)
        Rate.objects.increase_or_create(link, self.occurence)
        return link

    def connect_words_and_link(self, words, link):
        link.words.add(*words)
