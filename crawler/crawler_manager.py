#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils.timezone import datetime, make_aware
from crawler.reader_builder import ReaderBuilder
from crawler.items_saver import ItemSaver
from collections import namedtuple

SourceLink = namedtuple('SourceLink', ['link', 'source_name'])

sourcelinks = [
    SourceLink('http://wiadomosci.wp.pl/kat,1342,ver,rss,rss.xml', 'WP'),
    SourceLink('http://wiadomosci.wp.pl/kat,1356,ver,rss,rss.xml', 'WP'),
]


class CrawlerManager:

    def __init__(self):
        self.timestamp = make_aware(datetime.now())

    def crawl(self):
        for sourcelink in sourcelinks:
            itemsaver = ItemSaver(sourcelink.source_name, self.timestamp)
            try:
                reader = ReaderBuilder().get_reader(sourcelink.link)
                for address, title in reader.get_titles_and_addresses():
                    itemsaver.save_link_and_words(address, title)
            except NotImplementedError:
                continue
