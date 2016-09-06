#!/usr/bin/env python
# -*- coding: utf-8 -*-
from api.generic_list import GenericList
from core.models import Link


class LinksList(GenericList):
    list_class = Link
