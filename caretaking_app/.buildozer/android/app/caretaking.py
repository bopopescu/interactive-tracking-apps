from sqlalchemy import create_engine, Column, Integer, String,  ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Persisted = declarative_base()


class CareLog(Persisted):
    __tablename__ = 'logs'
    care_log_id = Column(Integer, primary_key=True)
    patients = relationship('Patient', uselist=True, secondary='observations')
    observations = relationship('Observation', uselist = True, back_populates='log')

class Patient(Persisted):
    __tablename__ = 'patients'
    patient_id = Column(Integer, primary_key=True)
    name = Column(String(256))
    care_log = relationship('CareLog', uselist=True, back_populates='patients', secondary='observations')
    observations = relationship('Observation', uselist = True, back_populates ='patient')


class Observation(Persisted):
    __tablename__ = 'observations'
    observation_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id'))
    care_log_id = Column(Integer, ForeignKey('logs.care_log_id'))
    location = Column(String(256))
    activity = Column(String(256))
    appetite = Column(String(256))
    birthdate = Column(String(256))
    city = Column(String(256))
    weight = Column(String(256))
    temperature = Column(String(256))
    date_time = Column(DateTime)
    log = relationship('CareLog', back_populates ='observations')
    patient = relationship('Patient', back_populates = 'observations')









class CareTakingDatabase(object):
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
