from kivy.app import App

# noinspection PyUnresolvedReferences
from sqlalchemy.exc import SQLAlchemyError
from sys import stderr
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from datetime import datetime
from pain_entries import MedicationEntry
from medication_entry_screen import MedicationEntryScreen
from choosing_entry import ChoosingEntry
from pain_entry_screen import PainEntryScreen
from pain_entries import PainMedicationDatabase, PainLocation, PainEntry, PainEntryLocation, Medicine


class MultipleScreenApp(App):

    def __init__(self, **kwargs):
        super(MultipleScreenApp, self).__init__(**kwargs)
        url = PainMedicationDatabase.construct_mysql_url('localhost', 3306, 'pain_tracking', 'root', 'cse')
        self.movie_database = PainMedicationDatabase(url)
        self.session = self.movie_database.create_session()

    def open_medication_entry_screen(self):
        self.root.transition.direction = 'right'
        self.root.current = 'third'

    def open_pain_entry_screen(self):
        self.root.transition.direction = 'left'
        self.root.current = 'second'

    def open_choosing_entry(self):
        self.root.transition.direction = 'right'
        self.root.current = 'first'

    def create_entry(self,head_selected, arm_selected, stomach_selected, leg_selected):
        try:
            arm = self.session.query(PainLocation).filter(PainLocation.body_location == 'Arm').one()
            head = self.session.query(PainLocation).filter(PainLocation.body_location == 'Head').one()
            leg = self.session.query(PainLocation).filter(PainLocation.body_location == 'Leg').one()
            stomach = self.session.query(PainLocation).filter(PainLocation.body_location == 'Stomach').one()

            location_list = []
            if arm_selected is True:
                location_list.append(arm)
            if head_selected is True:
                location_list.append(head)
            if leg_selected is True:
                location_list.append(leg)
            if stomach_selected is True:
                location_list.append(stomach)

            pain_entry = PainEntry(time_stamp= datetime.now(), locations=location_list)
            self.session.add(pain_entry)
            self.session.commit()

            #Bugged
            #self.root.ids.second.message.text = 'Entry Saved'

        except SQLAlchemyError as exception:
            print('Database setup failed!', file=stderr)
            print('Cause: {exception}'.format(exception=exception), file=stderr)
            #Bugged
            #self.root.ids.second.message.text = 'Coudln't connect to the database'
        except MultipleResultsFound as exception:
            print('Can not create multiple results found')
        except NoResultFound as exception:
            print('No results found')

    def save_medication(self, acetyl_selected, paracetamol_selected, ib_selected):
        try:
            acetyl = self.session.query(Medicine).filter(Medicine.medicine_type == 'Acetylsalicylic (mg)').one()
            paracetamol = self.session.query(Medicine).filter(Medicine.medicine_type == 'Paracetamol (ml)').one()
            ib = self.session.query(Medicine).filter(Medicine.medicine_type == 'Ibuprofen (mg)').one()

            med_list = []
            if acetyl_selected is True:
                med_list.append(acetyl)
            if paracetamol_selected is True:
                med_list.append(paracetamol)
            if ib_selected is True:
                med_list.append(ib)

            med_entry = MedicationEntry(time_stamp= datetime.now(), medicine=med_list)
            self.session.add(med_entry)
            self.session.commit()

            #Bugged
            #self.root.ids.second.message.text = 'Entry Saved'

        except SQLAlchemyError as exception:
            print('Database setup failed!', file=stderr)
            print('Cause: {exception}'.format(exception=exception), file=stderr)
            #self.root.ids.second.message.text = 'Coudln't connect to the database'
        except MultipleResultsFound as exception:
            print('Can not create multiple results found')
        except NoResultFound as exception:
            print('No results found')

def main():
    try:
        app = MultipleScreenApp()
        app.run()
    except SQLAlchemyError as exception:
        print('Initial database connection failed!', file=stderr)
        print('Cause: {exception}'.format(exception=exception), file=stderr)
        exit(1)


if __name__ == '__main__':
    main()
