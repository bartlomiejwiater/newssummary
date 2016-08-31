#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crawler.title_cleaner import TitleCleaner
import pytest


@pytest.mark.parametrize("test_input, expected", [
    ('Ile to trwa?', 'Ile to trwa'),
])
def test_titlecleaner_removes_unwanted_chars(test_input, expected):
    ts = TitleCleaner(test_input)
    clean_title = ts.clean()
    assert clean_title == expected
