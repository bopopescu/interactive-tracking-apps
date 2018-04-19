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

from pain_tracking_app.database import CombinedDatabase, PainLocation, PainEntryLocation, PainEntry, Medicine, MedicationEntry, MedicationEntryDosage


class MultipleScreenApp(App):

    def __init__(self, **kwargs):
        super(MultipleScreenApp, self).__init__(**kwargs)
        url = CombinedDatabase.construct_mysql_url('mysql.poetical-science.org', 3306, 'soft161_team_6', 'soft161_team_6', 'chromosome+differentiates<')
        self.pain_tracking_database = CombinedDatabase(url)
        self.session = self.pain_tracking_database.create_session()

    def open_medication_entry_screen(self):
        self.root.transition.direction = 'right'
        self.root.current = 'third'

    def open_pain_entry_screen(self):
        self.root.transition.direction = 'right'
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
        self.root.ids.third.ids.ibuprofen.state = 'normal'
        self.root.ids.third.ids.acetyl_comment.text = ''
        self.root.ids.third.ids.paracetamol_comment.text = ''
        self.root.ids.third.ids.ibuprofen_comment.text = ''
        self.root.ids.second.ids.report_entry.text = 'waiting'
        self.root.ids.third.ids.report_entry.text = 'waiting'

    @staticmethod
    def _pain_entry_severity(session, pain_entry, pain_location, severity):
        entry = session.query(PainEntryLocation).filter(PainEntryLocation.pain_id == pain_entry.pain_id,
                                                        PainEntryLocation.location_id == pain_location.location_id).first()
        entry.severity = severity
        session.add(entry)
        session.commit()

    def pain_entry(self, head_selected, arm_selected, stomach_selected, leg_selected):
        try:
            arm = self.session.query(PainLocation).filter(PainLocation.body_location == 'Arm').one()
            head = self.session.query(PainLocation).filter(PainLocation.body_location == 'Head').one()
            leg = self.session.query(PainLocation).filter(PainLocation.body_location == 'Leg').one()
            stomach = self.session.query(PainLocation).filter(PainLocation.body_location == 'Stomach').one()
            location_list = []
            severity_list = []
            if arm_selected:
                location_list.append(arm)
                severity_list.append(int(self.root.ids.second.ids.arm_severity.text))
            if head_selected:
                location_list.append(head)
                severity_list.append(int(self.root.ids.second.ids.head_severity.text))
            if leg_selected:
                location_list.append(leg)
                severity_list.append(int(self.root.ids.second.ids.leg_severity.text))
            if stomach_selected:
                location_list.append(stomach)
                severity_list.append(int(self.root.ids.second.ids.stomach_severity.text))
            pain_entry = PainEntry(time_stamp=datetime.now(), locations=location_list)
            self.session.add(pain_entry)
            self.session.commit()
            for x in range(len(location_list)):
                self._pain_entry_severity(self.session, pain_entry, location_list[x], severity_list[x])
            self.root.ids.second.ids.report_entry.text = 'Entry Saved'
        except SQLAlchemyError as exception:
            print('Database setup failed!', file=stderr)
            print('Cause: {exception}'.format(exception=exception), file=stderr)
            self.root.ids.second.ids.report_entry.text = 'Couldn\'t connect to the database'
        except MultipleResultsFound:
            print('Can not create multiple results found')
        except NoResultFound:
            print('No results found')

    def save_medication(self, acetyl_selected, paracetamol_selected, ib_selected):
        try:
            acetyl = self.session.query(Medicine).filter(Medicine.medicine_type == 'Acetylsalicylic (mg)').one()
            paracetamol = self.session.query(Medicine).filter(Medicine.medicine_type == 'Paracetamol (ml)').one()
            ibuprofen = self.session.query(Medicine).filter(Medicine.medicine_type == 'Ibuprofen (mg)').one()
            med_list = []
            dosage_list = []
            if acetyl_selected:
                med_list.append(acetyl)
                dosage_list.append(self.root.ids.third.ids.acetyl_comment.text)
            if paracetamol_selected:
                med_list.append(paracetamol)
                dosage_list.append(self.root.ids.third.ids.paracetamol_comment.text)
            if ib_selected:
                med_list.append(ibuprofen)
                dosage_list.append(self.root.ids.third.ids.ibuprofen_comment.text)
            med_entry = MedicationEntry(time_stamp=datetime.now(), medicines=med_list)
            self.session.add(med_entry)
            self.session.commit()
            for y in range(len(med_list)):
                self._medication_entry_dosage(self.session, med_entry, med_list[y], dosage_list[y])
            self.root.ids.third.ids.report_entry.text = 'Entry Saved'
        except SQLAlchemyError as exception:
            print('Database setup failed!', file=stderr)
            print('Cause: {exception}'.format(exception=exception), file=stderr)
            self.root.ids.third.report_entry.text = 'Coudldn\'t connect to the database'
        except MultipleResultsFound:
            print('Can not create multiple results found')
        except NoResultFound:
            print('No results found')

    @staticmethod
    def _medication_entry_dosage(session, medication, medicine, dosage):
        entry = session.query(MedicationEntryDosage).filter(MedicationEntryDosage.medication_id == medication.medication_id,
                                                            MedicationEntryDosage.medicine_id == medicine.medicine_id).first()
        entry.dosage = dosage
        session.add(entry)
        session.commit()

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
