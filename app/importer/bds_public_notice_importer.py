from time import mktime
import subprocess
import tempfile
import requests
from datetime import datetime
from .feed_importer import FeedImporter
from app.db import session
from app.models.channel import Channel
from sqlalchemy.orm.exc import NoResultFound


class BDSPublicNoticeImporter(FeedImporter):
    """https://www.portlandoregon.gov/bds/35625"""

    def get_text_from_pdf(self, link):
        pdf_text = ""
        try:
            response = requests.get(link)
            response.raise_for_status()

            with tempfile.NamedTemporaryFile() as tmp:
                tmp.write(response.content)
                sp = subprocess.run(['pdftotext', '-enc', 'UTF-8', '-raw', tmp.name, '-'],
                                    stdout=subprocess.PIPE)
                pdf_text = sp.stdout
        except requests.exceptions.HTTPError as err:
            pdf_text = ""

        return pdf_text

    def load_entry(self, entry):
        neighborhood, date, address, detail, case = [s.strip() for s in entry.title.split('|')]
        posted_at = datetime.fromtimestamp(mktime(entry.published_parsed))
        slug = Channel.generate_slug(posted_at, case)

        try:
            return session.query(Channel).filter_by(slug=slug).one(), False
        except NoResultFound:
            raw_text = self.get_text_from_pdf(entry.link)

            channel = Channel(
                name=self.name,
                posted_at=posted_at,
                neighborhood=neighborhood,
                address=address,
                description=detail,
                case=case,
                raw_text=raw_text)

            session.add(channel)
            session.commit()
