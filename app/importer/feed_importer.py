import feedparser
from app.db import session
from app.models.channel import Channel


class FeedImporter:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.process()

    def process(self):
        feed = feedparser.parse(self.url)
        for entry in feed.entries:
            self.load_entry(entry)

    def load_entry(self, entry):
        pass
