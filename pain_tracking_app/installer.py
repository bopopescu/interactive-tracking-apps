# -*- coding: utf-8; -*-

from sys import stderr
from sqlalchemy.exc import SQLAlchemyError
from tables import MedicationEntry,MedicationEntryDosage,PainEntryLocation,PainLocation,PainMedicationDatabase,\
    Medicine,PainEntry
import datetime


def add_starter_data(session):

    arm_location = PainLocation(body_location = 'Arm')
    leg_location = PainLocation(body_location = 'Leg')
    head_location = PainLocation(body_location = 'Head')
    stomach_location = PainLocation(body_location = 'Stomach')

    Acetyl = Medicine(medicine_type = 'Acetylsalicylic (mg)')
    paracetamol = Medicine(medicine_type = 'Paracetamol (ml)')
    Ibuprofen = Medicine(medicine_type = 'Ibuprofen (mg)')

    session.add(leg_location)
    session.add(arm_location)
    session.add(head_location)
    session.add(stomach_location)
    session.add(Acetyl)
    session.add(paracetamol)
    session.add(Ibuprofen)


def main():
    try:
        url = PainMedicationDatabase.construct_mysql_url('localhost', 3306, 'pain_tracking', 'root', 'cse')
        pain_tracking = PainMedicationDatabase(url)
        pain_tracking.ensure_tables_exist()
        print('Tables created.')
        session = pain_tracking.create_session()
        add_starter_data(session)
        session.commit()
        print('Records created.')
    except SQLAlchemyError as exception:
        print('Database setup failed!', file=stderr)
        print('Cause: {exception}'.format(exception=exception), file=stderr)
        exit(1)


if __name__ == '__main__':
    main()
