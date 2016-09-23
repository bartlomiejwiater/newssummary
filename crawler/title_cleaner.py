#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

unwanted_words = ['a', 'albo', 'ale', 'bo', 'by', 'był', 'co', 'czy', 'dla',
                  'dla', 'do', 'dot', 'dot.', 'go', 'gdy', 'gdzie', 'i', 'jak',
                  'jest', 'jest', 'już', 'lat', 'ma', 'mln', 'mln', 'na', 'na',
                  'nie', 'niż', 'niżej', 'o', 'od', 'ona', 'one', 'ono', 'po',
                  'r', 'r', 'się', 'są', 'tak', 'ten', 'to', 'tys', 'u', 'w',
                  'ws', 'ws.', 'z', 'za', 'ze', 'zł', 'że', 'ze']

unwanted_chars = [',', '.', '/', '?', ';', ':',
                  '(', ')', '!', '„', '”', '"', "'", '-']

DASH = re.compile('(?!<=[\d])-(?!lat|let|dni|mie)')
dot_or_colon = '(?!<=[\d]){0}(?![\d])'
DOT = re.compile(dot_or_colon.format('\.'))
COLON = re.compile(dot_or_colon.format(','))


class TitleCleaner:

    def __init__(self, title):
        self.title = title

    def clean(self):
        clean_title = self.clean_chars()
        clean_title = self.remove_trailing_spaces(clean_title)
        clean_title = self.clean_words(clean_title)
        return clean_title

    def clean_chars(self):
        title_copy = ''.join(self.title)
        for char in unwanted_chars:
            if '-' == char and char in title_copy:
                title_copy = re.sub(DASH, '', title_copy)
            elif (',' == char or '.' == char) and char in title_copy:
                accurate_pattern = DOT if '.' == char else COLON
                title_copy = re.sub(accurate_pattern, '', title_copy)
            else:
                title_copy = title_copy.replace(char, "")
        return title_copy

    def clean_words(self, title):
        titlewords = title.split()
        resultwords = [word for word in titlewords if word.lower()
                       not in unwanted_words]
        result = ' '.join(resultwords)
        return result

    def remove_trailing_spaces(self, title):
        return title.rstrip(' ')
