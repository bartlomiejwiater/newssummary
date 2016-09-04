#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import feedparser


class Reader:

    def __init__(self, link):
        self.link = link

    def open_link(self):
        print('opening... {}'.format(self.link))
        f = urllib.request.urlopen(self.link)
        source = f.read()
        return source


class RssReader(Reader):

    def get_titles_and_addresses(self):
        try:
            source = self.open_link()
        except urllib.error.URLError:
            print('Couldnt open {}'.format(self.link))
            return None
        tree = feedparser.parse(source)
        entries = tree['entries']
        for entry in entries:
            yield entry['link'], entry['title']
