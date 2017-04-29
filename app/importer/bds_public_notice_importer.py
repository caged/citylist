from time import mktime
from datetime import datetime
from .feed_importer import FeedImporter
from app.db import session
from app.models.channel import Channel
from sqlalchemy.orm.exc import NoResultFound


class BDSPublicNoticeImporter(FeedImporter):
    """https://www.portlandoregon.gov/bds/35625"""

    def load_entry(self, entry):
        neighborhood, date, address, detail, case = [s.strip() for s in entry.title.split('|')]
        posted_at = datetime.fromtimestamp(mktime(entry.published_parsed))

        slug = Channel.generate_slug(posted_at, case)

        try:
            return session.query(Channel).filter_by(slug=slug).one(), False
        except NoResultFound:
            channel = Channel(
                name=self.name,
                posted_at=posted_at,
                neighborhood=neighborhood,
                address=address,
                description=detail,
                case=case)

            session.add(channel)
            session.commit()
