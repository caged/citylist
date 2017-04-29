from sqlalchemy import Column, Integer, String, UnicodeText, DateTime
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
