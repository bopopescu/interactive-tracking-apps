from kivy.app import App
from sqlalchemy.exc import SQLAlchemyError
from sys import stderr
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from datetime import datetime
# noinspection PyUnresolvedReferences
from medication_entry import MedicationEntryScreen
# noinspection PyUnresolvedReferences
from choosing_entry import ChoosingEntry
# noinspection PyUnresolvedReferences
from pain_entry import PainEntryScreen

from installer.database import CombinedDatabase, PainLocation, PainEntryLocation, PainEntry, Medicine, MedicationEntry


class MultipleScreenApp(App):

    def __init__(self, **kwargs):
        super(MultipleScreenApp, self).__init__(**kwargs)
        url = CombinedDatabase.construct_mysql_url('localhost', 3306, 'pain_tracking', 'root', 'cse')
        self.movie_database = CombinedDatabase(url)
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
        self.root.ids.second.ids.head.state = 'normal'
        self.root.ids.second.ids.arm.state = 'normal'
        self.root.ids.second.ids.stomach.state = 'normal'
        self.root.ids.second.ids.leg.state = 'normal'
        self.root.ids.second.ids.head_severity.text = '1'
        self.root.ids.second.ids.arm_severity.text = '1'
        self.root.ids.second.ids.stomach_severity.text = '1'
        self.root.ids.second.ids.leg_severity.text = '1'
        self.root.ids.third.ids.acetyl.state = 'normal'
        self.root.ids.third.ids.paracetamol.state = 'normal'
        self.root.ids.third.ids.Ib.state = 'normal'

    def pain_entry(self, head_selected, arm_selected, stomach_selected, leg_selected):
        try:
            arm = self.session.query(PainLocation).filter(PainLocation.body_location == 'Arm').one()
            head = self.session.query(PainLocation).filter(PainLocation.body_location == 'Head').one()
            leg = self.session.query(PainLocation).filter(PainLocation.body_location == 'Leg').one()
            stomach = self.session.query(PainLocation).filter(PainLocation.body_location == 'Stomach').one()
            location_list = []
            if arm_selected is True:
                location_list.append(arm)
                arm_severity = self.session.query(PainEntryLocation.severity).filter(PainLocation.body_location == 'Arm')
            if head_selected is True:
                location_list.append(head)
            if leg_selected is True:
                location_list.append(leg)
            if stomach_selected is True:
                location_list.append(stomach)
            pain_entry = PainEntry(time_stamp=datetime.now(), locations=location_list)
            self.session.add(pain_entry)
            self.session.commit()

            #Bugged
            #self.root.ids.second.message.text = 'Entry Saved'

        except SQLAlchemyError as exception:
            print('Database setup failed!', file=stderr)
            print('Cause: {exception}'.format(exception=exception), file=stderr)
            #Bugged
            #self.root.ids.second.message.text = 'Couldn't connect to the database'
        except MultipleResultsFound:
            print('Can not create multiple results found')
        except NoResultFound:
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

            med_entry = MedicationEntry(time_stamp=datetime.now(), medicine=med_list)
            self.session.add(med_entry)
            self.session.commit()

            #Bugged
            #self.root.ids.second.message.text = 'Entry Saved'

        except SQLAlchemyError as exception:
            print('Database setup failed!', file=stderr)
            print('Cause: {exception}'.format(exception=exception), file=stderr)
            #self.root.ids.second.message.text = 'Coudldn't connect to the database'
        except MultipleResultsFound:
            print('Can not create multiple results found')
        except NoResultFound:
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
