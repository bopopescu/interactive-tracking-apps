from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Persisted = declarative_base()


class Visit(Persisted):
    __tablename__ = 'visits'
    visit_id = Column(Integer, primary_key=True, autoincrement=True)
    date_time = Column(DATETIME, nullable=False)
    location = relationship('Location', back_populates='visit')
    health_factors = relationship('HealthFactor', uselist=True, secondary='visit_factors')


class Location(Persisted):
    __tablename__ = 'locations'
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    visit_id = Column(Integer, ForeignKey('visits.visit_id'))
    name = Column(String(256), nullable=False)
    visit = relationship('Visit', back_populates='location')
    health_facilities = relationship('Facility', uselist=True, back_populates='location')


class Facility(Persisted):
    __tablename__ = 'facilities'
    facility_id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey('locations.location_id'))
    name = Column(String(256), nullable=False)
    location = relationship('Location', back_populates='health_facilities')


class HealthFactor(Persisted):
    __tablename__ = 'health_factors'
    factor_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    comment = Column(String(512))
    visits = relationship('Visit', uselist=True, secondary='visit_factors')


class VisitFactors(Persisted):
    __tablename__ = 'visit_factors'
    visit_id = Column(Integer, ForeignKey('visits.visit_id'), primary_key=True)
    factor_id = Column(Integer, ForeignKey('health_factors.factor_id'), primary_key=True)


class VisitDatabase(object):
    @staticmethod
    def construct_mysql_url(authority, port, database, username, password):
        return 'mysql+mysqlconnector://{username}:{password}@{authority}:{port}/{database}' \
            .format(authority=authority, port=port, database=database, username=username, password=password)

    @staticmethod
    def construct_in_memory_url():
        return 'sqlite:///'

    def __init__(self, url):
        self.engine = create_engine(url)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    def ensure_tables_exist(self):
        Persisted.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()
