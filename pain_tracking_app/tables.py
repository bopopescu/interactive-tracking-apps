from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Persisted = declarative_base()


class PainEntry(Persisted):
    __tablename__ = 'pain_entry'
    pain_id = Column(Integer, primary_key=True)
    time_stamp = Column(Date, nullable=False)
    locations = relationship('PainLocation', uselist=True, secondary='pain_entry_location')
    # pain_location = relationship('PainLocation',uselist = True, secondary='pain_entry_location')


class PainLocation(Persisted):
    __tablename__ = 'locations'
    location_id = Column(Integer, primary_key=True)
    body_location = Column(String(256), nullable = False)
    pain_entry = relationship('PainEntry', uselist=True, secondary='pain_entry_location')
    # pain_entry_location = relationship('PainEntryLocation', back_populates = 'locations')


class PainEntryLocation(Persisted):
    __tablename__ = 'pain_entry_location'
    pain_id = Column(Integer, ForeignKey('pain_entry.pain_id'), primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.location_id'), primary_key= True)
    severity = Column(Integer)
    # pain_entry = relationship('PainEntry')
    # pain_location = relationship('PainLocation')


class MedicationEntry(Persisted):
    __tablename__ = 'medication_entry'
    medication_id = Column(Integer, primary_key=True)
    time_stamp = Column(Date, nullable=False)
    medicine = relationship('Medicine', uselist=True, secondary='medication_entry_dosage')
    #medication_entry_dosage = relationship('MedicationEntryDosage', uselist = True, back_populates='medication_entry')


class Medicine(Persisted):
    __tablename__ = 'medicine'
    medicine_id = Column(Integer, primary_key=True)
    medicine_type = Column(String(256), nullable = False)
    medication_entry = relationship('MedicationEntry', uselist=True, secondary='medication_entry_dosage')


class MedicationEntryDosage(Persisted):
    __tablename__ = 'medication_entry_dosage'
    medication_id = Column(Integer, ForeignKey('medication_entry.medication_id'), primary_key=True)
    medicine_id = Column(Integer, ForeignKey('medicine.medicine_id'), primary_key=True)
    dosage = Column(Integer)
    #medicine = relationship('Medicine', back_populates='medication_entry_dosage')
    #medication_entry = relationship('MedicationEntry', back_populates='medication_entry_dosage')


class PainMedicationDatabase(object):
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
