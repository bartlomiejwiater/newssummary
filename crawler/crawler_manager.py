#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils.timezone import datetime, make_aware
from crawler.reader_builder import ReaderBuilder
from crawler.items_saver import ItemSaver
from collections import namedtuple

sl = namedtuple('SourceLink', ['link', 'source_name'])

sourcelinks = [
    sl('http://www.bankier.pl/rss/wiadomosci.xml', 'BANKIER'),
    sl('http://www.gazetaprawna.pl/rss.xml', 'GAZETAPRAWNA'),
    sl('http://gosc.pl/rss/rtr/c7a21.Aktualnosci-z-Gosciem-Niedzielnym', 'GOŚĆNIEDZIELNY'),
    sl('http://fakty.interia.pl/polska/feed', 'INTERIA'),
    sl('http://www.money.pl/rss/main.xml', 'MONEY.PL'),
    sl('http://www.polsatnews.pl/rss/kraj.xml', 'POLSAT'),
    sl('http://www.rmf24.pl/fakty/polska/feed', 'RMF24'),
    sl('http://www.tokfm.pl/pub/rss/tokfmpl_polska.xml', 'TOKFM'),
    sl('http://www.tvn24.pl/najnowsze.xml', 'TVN24'),
    sl('http://www.tvn24.pl/najwazniejsze.xml', 'TVN24'),
    sl('http://www.tvp.info/tvp.info/rss+xml.php?object_id=191865', 'TVPINFO'),
    sl('http://wiadomosci.wp.pl/kat,1342,ver,rss,rss.xml', 'WP'),
    sl('http://wiadomosci.wp.pl/kat,1356,ver,rss,rss.xml', 'WP'),
    sl('http://serwisy.gazeta.pl/pub/rss/najnowsze_wyborcza.xml', 'WYBORCZA'),
    sl('http://forsal.pl/atom/najnowsze', 'FORSAL'),
    sl('http://forsal.pl/atom/forsal', 'FORSAL')
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
                print('Did not get Reader for {}'.format(sourcelink.link))
                continue
