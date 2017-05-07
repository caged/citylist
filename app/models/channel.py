from datetime import datetime
import re
import sqlalchemy as sa
from sqlalchemy import event, orm
from app.db import Base
import geocoder
import textwrap


class Channel(Base):
    __tablename__ = 'channels'

    id = sa.Column(sa.Integer, primary_key=True)
    slug = sa.Column(sa.Text)
    name = sa.Column(sa.Text)
    case = sa.Column(sa.Text)
    link = sa.Column(sa.Text)
    posted_at = sa.Column(sa.DateTime)
    imported_at = sa.Column(sa.DateTime)
    neighborhood = sa.Column(sa.Text)
    address = sa.Column(sa.Text)
    lat = sa.Column(sa.REAL)
    lon = sa.Column(sa.REAL)
    description = sa.Column(sa.Text)
    raw_text = sa.Column(sa.Text)

    @orm.reconstructor
    def init_on_load(self):
        self.proposal = self.extract_proposal()
        self.excerpt = self.extract_proposal_excerpt()
        try:
            self.title, self.notice = self.description.split(' - ')
            self.notice_class = self.notice.lower().replace(' ', '-')
        except:
            self.title = self.description

    def extract_proposal(self):
        val = re.sub('\\n', '', self.raw_text)
        try:
            return re.split('proposal:', val, flags=re.IGNORECASE)[1]
        except Exception as e:
            ""

    def extract_proposal_excerpt(self):
        return textwrap.shorten(self.proposal, width=350)

    @classmethod
    def generate_slug(cls, date, case):
        return date.strftime('%s') + ''.join(case.split()).lower()


@event.listens_for(Channel, 'before_insert')
def set_slug(mapper, connect, self):
    self.slug = self.posted_at.strftime('%s') + ''.join(self.case.split()).lower()
    self.imported_at = datetime.now()


@event.listens_for(Channel.address, 'set')
def set_lat_lon(target, value, oldvalue, initiator):
    g = geocoder.google(value + " Portland, OR")
    if g.ok:
        target.lat = g.latlng[0]
        target.lon = g.latlng[1]
