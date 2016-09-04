#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crawler.readers import RssReader


class ReaderBuilder:

    def get_reader(self, link):
        if link.endswith('.rss') or link.endswith('.xml'):
            return RssReader(link)
        else:
            raise NotImplementedError
