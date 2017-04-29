from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
engine = create_engine('sqlite:///app/citylist.db', echo=True)
Session.configure(bind=engine)
Base = declarative_base()

session = Session()
