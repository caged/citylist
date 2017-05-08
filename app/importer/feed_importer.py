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
            try:
                self.load_entry(entry)
            except:
                print("Unable to load %s at %s" % (entry.title, self.url))

    def load_entry(self, entry):
        pass
