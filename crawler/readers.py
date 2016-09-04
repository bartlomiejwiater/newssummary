import urllib.request
import feedparser


class Reader:

    def __init__(self, link):
        self.link = link

    def open_link(self):
        f = urllib.request.urlopen(self.link)
        source = f.read()
        return source


class RssReader(Reader):

    def get_titles_and_addresses(self):
        source = self.open_link()
        tree = feedparser.parse(source)
        entries = tree['entries']
        for entry in entries:
            yield entry['link'], entry['title']
