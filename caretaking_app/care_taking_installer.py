from __future__ import print_function


from sqlalchemy.exc import SQLAlchemyError
from caretaking import CareTakingDatabase, Patient, CareLog, Observation, User
from datetime import datetime


def add_starter_data(session):
    charles = User(user_id='10002T')
    jon_smith = Patient(name='Jon Smith', user_id='10002T')
    session.add(charles)

    session.add(jon_smith)
    robert_kennedy = Patient(name='Robert Kennedy', user_id='10002T')
    session.add(robert_kennedy)
    george_washington=Patient(name='George Washington', user_id='10001V')
    session.add(george_washington)

    care_log = CareLog()

    jon_obs = Observation(patient= jon_smith,log = care_log,location='Patient Home', activity='5-Very Active', appetite = '5-Very Healthy', birthdate='05/04/1998', city ='Omaha', weight='120', temperature='50', date_time=datetime(2018,4,12,20,11,12,13))
    session.add(jon_obs)

    care_log1 = CareLog()

    robert = Observation(patient= robert_kennedy,log = care_log1,location='Patient Home', activity='5-Very Active', appetite = '5-Very Healthy', birthdate='05/04/1998', city ='Omaha', weight='120', temperature='50', date_time=datetime(2018,4,12,20,11,12,13))
    session.add(robert)

    care_log2 = CareLog()

    george = Observation(patient= george_washington,log = care_log2,location='Hospital', activity='5-Very Active', appetite = '5-Very Healthy', birthdate='05/04/1998', city ='Omaha', weight='120', temperature='50', date_time=datetime(2018,4,12,20,11,12,13))
    session.add(george)







def main():
    try:
        url = CareTakingDatabase.construct_mysql_url('localhost', 3306, 'CareLog', 'root', 'cse')
        care_taking_database = CareTakingDatabase(url)
        care_taking_database.ensure_tables_exist()
        print('Tables created.')
        session = care_taking_database.create_session()
        add_starter_data(session)
        session.commit()
        print('Records created.')
    except SQLAlchemyError as exception:
        print('Database setup failed!')
        print('Cause: {exception}'.format(exception=exception))
        exit(1)
if __name__ == '__main__':
    main()
