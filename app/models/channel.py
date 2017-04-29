from datetime import datetime
from sqlalchemy import Column, Integer, String, UnicodeText, DateTime
from sqlalchemy import event
from app.db import Base


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)
    slug = Column(String)
    name = Column(UnicodeText)
    posted_at = Column(DateTime)
    imported_at = Column(DateTime)
    neighborhood = Column(UnicodeText)
    address = Column(UnicodeText)
    description = Column(UnicodeText)
    case = Column(UnicodeText)
    raw_text = Column(UnicodeText)

    @classmethod
    def generate_slug(cls, date, case):
        return date.strftime('%s') + ''.join(case.split()).lower()


@event.listens_for(Channel, 'before_insert')
def set_slug(mapper, connect, self):
    self.slug = self.posted_at.strftime('%s') + ''.join(self.case.split()).lower()
    self.imported_at = datetime.now()
