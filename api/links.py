#!/usr/bin/env python
# -*- coding: utf-8 -*-
from api.generic_list import GenericList
from core.models import Link


class LinksList(GenericList):
    list_class = Link

    def fiter_links_according_to_word(self, links, wanted_words):
        return links.filter(words__name__in=wanted_words)
