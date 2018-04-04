from visit_tables import VisitDatabase, Location, Facility, HealthFactor
from sqlalchemy.exc import SQLAlchemyError
from sys import stderr


def add_table_data(session):
    lincoln = Location(name='Lincoln, NE')
    omaha = Location(name='Omaha, NE')
    columbus = Location(name='Columbus, NE')
    pediatric_lincoln = Facility(name='Pediatric Hospital', location=lincoln)
    community_lincoln = Facility(name='Community Hospital', location=lincoln)
    lakeside_omaha = Facility(name='Lakeside Hospital', location=omaha)
    unmc_omaha = Facility(name='UNMC', location=omaha)
    urgent_columbus = Facility(name='Urgent Care', location=columbus)
    chicken_pox = HealthFactor(name='Chicken Pox', comment='Irritable, Rashes')
    fever = HealthFactor(name='Fever')
    coughing = HealthFactor(name='Coughing', comment='Persistent for two weeks')
    muscle_aches = HealthFactor(name='Muscle Aches', comment='Weakness in legs and back')
    diarrhea = HealthFactor(name='Severe Diarrhea')
    vomiting = HealthFactor(name='Vomiting', comment='Lasted for a whole day')
    session.add(lincoln)
    session.add(omaha)
    session.add(columbus)
    session.add(pediatric_lincoln)
    session.add(community_lincoln)
    session.add(lakeside_omaha)
    session.add(unmc_omaha)
    session.add(urgent_columbus)
    session.add(chicken_pox)
    session.add(fever)
    session.add(coughing)
    session.add(muscle_aches)
    session.add(diarrhea)
    session.add(vomiting)


def main():
    try:
        url = VisitDatabase.construct_mysql_url('localhost', 3306, 'visit', 'root', 'cse')
        visit_database = VisitDatabase(url)
        visit_database.ensure_tables_exist()
        print('Tables created.')
        session = visit_database.create_session()
        add_table_data(session)
        session.commit()
        print('Tables have been populated.')
    except SQLAlchemyError:
        print('Database setup failed! Please test your connection and try again.', file=stderr)
        exit(1)

if __name__ == '__main__':
    main()
