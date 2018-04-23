from unittest import TestCase
# noinspection PyUnresolvedReferences
from main import MultipleScreenApp
# noinspection PyUnresolvedReferences
from database import CombinedDatabase, PainLocation, PainEntryLocation, Patient, PainEntry
# noinspection PyUnresolvedReferences
from datetime import datetime
# noinspection PyUnresolvedReferences


class MyTestCase(TestCase):

    def test_insert_pain(self):
        url = CombinedDatabase.construct_in_memory_url()
        pain_entry_database = CombinedDatabase(url)
        pain_entry_database.ensure_tables_exist()
        session = pain_entry_database.create_session()

        pain_entry = PainEntry(time_stamp=datetime.now(), locations=location_list)
        MultipleScreenApp._pain_entry_severity(session, pain_entry, arm, 6)
        actual = session.query(PainEntryLocation).filter(PainEntryLocation.pain_location == 'Arm').one()
        self.assertEqual(actual.pain_entry, pain_entry)
        self.assertEqual(actual.severity, 6)

    def test_insert_null_pain(self):
        url = PainMedicationDatabase.construct_in_memory_url()
        pain_entry_database = PainMedicationDatabase(url)
        pain_entry_database.ensure_tables_exist()
        session = pain_entry_database.create_session()
        location_list = []
        severity_list = []
        pain_entry = PainEntry(time_stamp=datetime.now(), locations=location_list)
        MultipleScreenApp._pain_entry_severity(session, pain_entry, '', '')
        actual = session.query(PainEntryLocation).filter(PainEntryLocation.pain_location == '').one()
        self.assertEqual(actual.severity, '')

    def test_insert_multiple_pain(self):
        url = PainMedicationDatabase.construct_in_memory_url()
        pain_entry_database = PainMedicationDatabase(url)
        pain_entry_database.ensure_tables_exist()
        session = pain_entry_database.create_session()
        arm = session.query(PainLocation).filter(PainLocation.body_location == 'Arm').count()
        head = session.query(PainLocation).filter(PainLocation.body_location == 'Head').count()
        location_list = []
        location_list.append(arm)
        location_list.append(head)
        severity_list = []
        severity_list.append(7)
        severity_list.append(8)
        pain_entry = PainEntry(time_stamp=datetime.now(), locations=location_list)
        MultipleScreenApp._pain_entry_severity(session, pain_entry, arm, 7)
        actual = session.query(PainEntryLocation).filter(PainEntryLocation.pain_location == 'Arm').one()
        self.assertEqual(actual.severity, 7)
        MultipleScreenApp._pain_entry_severity(session, pain_entry, head, 7)
        actual = session.query(PainEntryLocation).filter(PainEntryLocation.pain_location == 'Arm').one()
        self.assertEqual(actual.severity, 8)

    def test_insert_medication(self):
        url = PainMedicationDatabase.construct_in_memory_url()
        medication_entry_database = PainMedicationDatabase(url)
        medication_entry_database.ensure_tables_exist()
        session = medication_entry_database.create_session()
        acetyl = session.query(Medicine).filter(Medicine.medicine_type == 'Acetylsalicylic (mg)').count()
        dosage_list = []
        dosage_list.append(20)
        MultipleScreenApp._medication_entry_dosage(session, '', acetyl, 20)
