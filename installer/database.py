from sqlalchemy import create_engine, Column, Integer, String,  ForeignKey, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Persisted = declarative_base()


class CareLog(Persisted):
    __tablename__ = 'logs'
    care_log_id = Column(Integer, primary_key=True)
    patients = relationship('Patient', uselist=True, secondary='observations')
    observations = relationship('Observation', uselist=True, back_populates='log')


class Observation(Persisted):
    __tablename__ = 'observations'
    observation_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id'))
    care_log_id = Column(Integer, ForeignKey('logs.care_log_id'))
    location = Column(String(256))
    activity = Column(String(256))
    appetite = Column(String(256))
    birth_date = Column(String(256))
    city = Column(String(256))
    weight = Column(String(256))
    temperature = Column(String(256))
    date_time = Column(DateTime)
    log = relationship('CareLog', back_populates='observations')
    patient = relationship('Patient', back_populates='observations')


class PainEntry(Persisted):
    __tablename__ = 'pain_entry'
    pain_id = Column(Integer, primary_key=True)
    time_stamp = Column(Date, nullable=False)
    locations = relationship('PainLocation', uselist=True, secondary='pain_entry_location')
    pain_entry_location = relationship('PainEntryLocation', uselist=True, back_populates='pain_entry')


class PainLocation(Persisted):
    __tablename__ = 'locations'
    location_id = Column(Integer, primary_key=True)
    body_location = Column(String(256), nullable=False)
    pain_entries = relationship('PainEntry', uselist=True, secondary='pain_entry_location')
    pain_entry_location = relationship('PainEntryLocation', uselist=True, back_populates='pain_location')


class PainEntryLocation(Persisted):
    __tablename__ = 'pain_entry_location'
    pain_id = Column(Integer, ForeignKey('pain_entry.pain_id'), primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.location_id'), primary_key=True)
    severity = Column(Integer)
    pain_entry = relationship('PainEntry', back_populates='pain_entry_location')
    pain_location = relationship('PainLocation', back_populates='pain_entry_location')


class MedicationEntry(Persisted):
    __tablename__ = 'medication_entry'
    medication_id = Column(Integer, primary_key=True)
    time_stamp = Column(Date, nullable=False)
    medicines = relationship('Medicine', uselist=True, secondary='medication_entry_dosage')
    medication_dosage = relationship('MedicationEntryDosage', uselist=True, back_populates='medication_entry')


class Medicine(Persisted):
    __tablename__ = 'medicine'
    medicine_id = Column(Integer, primary_key=True)
    medicine_type = Column(String(256), nullable=False)
    medication_entries = relationship('MedicationEntry', uselist=True, secondary='medication_entry_dosage')
    medication_dosage = relationship('MedicationEntryDosage', uselist=True, back_populates='medicine')


class MedicationEntryDosage(Persisted):
    __tablename__ = 'medication_entry_dosage'
    medication_id = Column(Integer, ForeignKey('medication_entry.medication_id'), primary_key=True)
    medicine_id = Column(Integer, ForeignKey('medicine.medicine_id'), primary_key=True)
    dosage = Column(Integer)
    medicine = relationship('Medicine', back_populates='medication_dosage')
    medication_entry = relationship('MedicationEntry', back_populates='medication_dosage')


class User(Persisted):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    Open_MRS_ID = Column(String(256))
    surname = Column(String(256), nullable=False)
    given_name = Column(String(256), nullable=False)
    patient = relationship('Patient', back_populates='user')


class Patient(Persisted):
    __tablename__ = 'patients'
    patient_id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    name = Column(String(256))
    user_id = Column(String(256), ForeignKey('users.user_id'))
    user = relationship('User', back_populates='patient')
    observations = relationship('Observation', uselist=True, back_populates='patient')


class CombinedDatabase(object):
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
