#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crawler.readers import RssReader


class ReaderBuilder:

    def get_reader(self, link):
        if link.endswith('.rss') or link.endswith('.xml'):
            return RssReader(link)
        elif ('rmf24' in link or 'interia' in link) and 'feed' in link:
            return RssReader(link)
        elif 'tvp.info' in link:
            return RssReader(link)
        elif 'rss' in link and 'gosc.pl' in link:
            return RssReader(link)
        else:
            raise NotImplementedError
