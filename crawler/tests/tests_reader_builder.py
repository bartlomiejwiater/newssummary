from crawler.reader_builder import ReaderBuilder
from crawler.readers import RssReader
import pytest


@pytest.mark.parametrize("test_link_input, expected_class",
                         [
                             ('http://source.pl/rss.xml', RssReader),
                             ('http://source.pl/news.rss', RssReader),
                         ])
def test_reader_builder_returns_proper_class(test_link_input, expected_class):
    result = ReaderBuilder().get_reader(test_link_input)
    assert isinstance(result, expected_class)


def test_reader_builder_raise_NotImplementedError():
    with pytest.raises(NotImplementedError):
        ReaderBuilder().get_reader('http://source.pl/rss.doc')
