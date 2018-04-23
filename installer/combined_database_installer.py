from __future__ import print_function


from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from database import CareLog, Observation, PainLocation, Medicine, CombinedDatabase, Patient, User


def add_starter_data(session):
    jon_smith = Patient(name='Jon Smith')
    session.add(jon_smith)
    robert_kennedy = Patient(name='Robert Kennedy')
    session.add(robert_kennedy)
    george_washington=Patient(name='George Washington')
    session.add(george_washington)
    ada_lovelace = User(given_name='Ada', surname='Lovelace', user_id='10001V')
    session.add(ada_lovelace)
    charles_babbage = User(given_name='Charles', surname='Babbage', user_id='10000X')
    session.add(charles_babbage)

    care_log = CareLog()
    jon_obs = Observation(patient= jon_smith, log=care_log,location='Patient Home', activity='5-Very Active', appetite = '5-Very Healthy', birth_date='05/04/1998', city ='Omaha', weight='120', temperature='50', date_time=datetime(2018, 4, 12, 20, 11, 12, 13))
    session.add(jon_obs)

    care_log1 = CareLog()
    robert = Observation(patient= robert_kennedy, log=care_log1, location='Patient Home', activity='5-Very Active', appetite = '5-Very Healthy', birth_date='05/04/1998', city ='Omaha', weight='120', temperature='50', date_time=datetime(2018, 4, 12, 20, 11, 12, 13))
    session.add(robert)

    arm_location = PainLocation(body_location='Arm')
    leg_location = PainLocation(body_location='Leg')
    head_location = PainLocation(body_location='Head')
    stomach_location = PainLocation(body_location='Stomach')

    Acetyl = Medicine(medicine_type='Acetylsalicylic (mg)')
    paracetamol = Medicine(medicine_type='Paracetamol (ml)')
    Ibuprofen = Medicine(medicine_type='Ibuprofen (mg)')

    session.add(leg_location)
    session.add(arm_location)
    session.add(head_location)
    session.add(stomach_location)
    session.add(Acetyl)
    session.add(paracetamol)
    session.add(Ibuprofen)


def main():
    try:
        url = CombinedDatabase.construct_mysql_url('mysql.poetical-science.org', 3306, 'soft161_team_6', 'soft161_team_6', 'chromosome+differentiates<')
        combined_database = CombinedDatabase(url)
        combined_database.ensure_tables_exist()
        print('Tables created.')
        session = combined_database.create_session()
        add_starter_data(session)
        session.commit()
        print('Records created.')
    except SQLAlchemyError as exception:
        print('Database setup failed!')
        print('Cause: {exception}'.format(exception=exception))
        exit(1)

if __name__ == '__main__':
    main()
