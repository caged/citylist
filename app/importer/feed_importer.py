import feedparser
from app.db import session
from app.models.channel import Channel


class FeedImporter:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def process(self):
        feed = feedparser.parse(url)
        for entry in feed.entries:
            load_entry(entry)

    def load_entry(self, entry):
        print(entry.description)
        # pass
