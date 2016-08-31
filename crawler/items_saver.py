#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.models import Occurence, Link, Word


class ItemSaver:

    def __init__(self, source, timestamp):
        self.source = source
        self.timestamp = timestamp
        self.occurence = None

    def save_link_and_words(self, address, title):
        if not self.occurence:
            self.get_or_create_occurence()

        clean_title = self.clean_title(title)
        word_objects = self.save_word(clean_title)
        link = self.save_and_return_link(address, title, word_objects)

    def get_or_create_occurence(self):
        self.occurence = Occurence.objects.get_or_create(timestamp=self.timestamp, source=self.source)

    def clean_title(self, title):
        clean_title = title
        return title

    def save_word(self, clean_title):
        word_objects = []
        for word in clean_title.split(' '):
            word_object, stat = Word.objects.get_or_create(name=word)
            word_objects.append(word_object)
        return word_objects

    def save_and_return_link(self, address, title, words_to_connect):
        link, o = Link.objects.get_or_create(address=address, title=title)

        for word in words_to_connect:
            link.words.add(word)
        return link
