from datetime import datetime
from urllib.request import pathname2url
import re
import shutil
import textwrap
import os
import sqlalchemy as sa
from sqlalchemy import event, orm
from app.db import Base
import geocoder
import requests

public_token = 'pk.eyJ1IjoiY2FnZWQiLCJhIjoiQjd2aXNGYyJ9.gr1QeGYwG1QYUW47I-DqaQ'


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

    def cached_map_image(self, width=300, height=300, zoom=14, pitch=0, bearing=0,
                         default='/static/tiles/na.png'):

        name = '%s-%s-%s-%s-%s-%s.png' % (self.id, width, height, zoom, pitch, bearing)
        file_name = '/static/tiles/%s' % name
        if os.path.isfile('app' + file_name):
            return file_name
        else:
            file_name = default

        try:
            geojson = self.geojson_point()
            url = "https://api.mapbox.com/styles/v1/mapbox/streets-v10/static/geojson(%s)/%s,%s,%s,%s,%s/%sx%s@2x?access_token=%s" % (
                pathname2url(geojson),
                self.lon,
                self.lat,
                zoom,
                bearing,
                pitch,
                width,
                height,
                public_token
            )

            print(url)
            img = requests.get(url)

            if img.status_code == 200:
                name = '%s-%s-%s-%s-%s-%s.png' % (self.id, width, height, zoom, pitch, bearing)
                file_name = '/static/tiles/%s' % name
                with open('app' + file_name, 'wb') as f:
                    f.write(img.content)

            return file_name

        except Exception as e:
            raise


    def geojson_point(self):
        return '{"type": "Point","coordinates": [%s, %s]}' % (self.lon, self.lat)

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
