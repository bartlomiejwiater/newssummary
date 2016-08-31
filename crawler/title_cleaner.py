#!/usr/bin/env python
# -*- coding: utf-8 -*-

unwanted_words = ['a', 'albo', 'ale', 'bo', 'by', 'był', 'co', 'czy', 'dla',
                  'dla', 'do', 'do', 'dot', 'dot.', 'gdy', 'gdzie', 'i', 'jak',
                  'jest', 'jest', 'już', 'lat', 'ma', 'mln', 'mln', 'na', 'na',
                  'nie', 'niż', 'niżej', 'o', 'od', 'ona', 'one', 'ono', 'po',
                  'r', 'r', 'się', 'są', 'tak', 'ten', 'to', 'tys', 'u', 'w',
                  'ws', 'ws.', 'z', 'za', 'ze', 'zł', 'że']

unwanted_chars = [',', '.', '/', '?', ';', ':', '(', ')', '!', '"', "'", '-']


class TitleCleaner:

    def __init__(self, title):
        self.title = title

    def clean(self):
        clean_title = self.clean_chars()
        return clean_title

    def clean_chars(self):
        title_copy = ''.join(self.title)
        for char in unwanted_chars:
            title_copy = title_copy.replace(char, "")
        return title_copy

    def clean_words(self):
        pass
