#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crawler.title_cleaner import TitleCleaner
import pytest


@pytest.mark.parametrize("test_input, expected", [
    ('Elity muszą ze sobą rywalizować', 'Elity muszą sobą rywalizować'),
    ('Trzęsienie ziemi w USA. Wstrząsy o sile 5,6 w skali Richtera w stanie Oklahoma',
     'Trzęsienie ziemi USA Wstrząsy sile 5,6 skali Richtera stanie Oklahoma'),
    ('Porwano go, żeby uczył dyktatora angielskiego',
     'Porwano żeby uczył dyktatora angielskiego'),
    ('5-latka wypadła z balkonu. Złapała ją przechodząca obok kobieta.',
     '5-latka wypadła balkonu Złapała ją przechodząca obok kobieta'),
    ('5-latka 15-latka latka -',
     '5-latka 15-latka latka'),
    ('Od dwóch lat zmniejsza się w Polsce stopa bezrobocia. W II kw. 2016 r., według danych Eurostat i GUS (BAEL), wynosiła 6,2 proc. ',
     'dwóch zmniejsza Polsce stopa bezrobocia II kw 2016 według danych Eurostat GUS BAEL wynosiła 6,2 proc',)

])
def test_titlecleaner_removes_unwanted_chars_and_words(test_input, expected):
    ts = TitleCleaner(test_input)
    clean_title = ts.clean()
    assert clean_title == expected
