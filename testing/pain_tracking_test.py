import unittest
from soft161_milestone_2.pain_tracking_app.main import MultipleScreenApp
from soft161_milestone_2.pain_tracking_app.tables import PainMedicationDatabase
from datetime import datetime
from soft161_milestone_2.installer.database import PainEntry, PainLocation, PainEntryLocation


class MyTestCase(unittest.TestCase):
    def test_open_medication_entry_screen(self):
        screen = self.root.current = 'first'
        MultipleScreenApp.open_medication_entry_screen(screen)
        self.assertEqual(self.root.current, 'third')

    def test_insert_pain(self):
        url = PainMedicationDatabase.construct_in_memory_url()
        pain_entry_database = PainMedicationDatabase(url)
        pain_entry_database.ensure_tables_exist()
        session = pain_entry_database.create_session()
        arm = self.session.query(PainLocation).filter(PainLocation.body_location == 'Arm').one()
        location_list = []
        location_list.append(arm)
        severity_list = []
        severity_list.append(6)
        pain_entry = PainEntry(time_stamp=datetime.now(), locations=location_list)
        MultipleScreenApp._pain_entry_severity(session, pain_entry, 'Arm', 6)
        actual = session.query(PainEntryLocation).filter(PainEntryLocation.pain_location == 'Arm').one()
        self.assertEqual(actual.severity, 6)

    def test_insert_null(self):
        url = PainMedicationDatabase.construct_in_memory_url()
        pain_entry_database = PainMedicationDatabase(url)
        pain_entry_database.ensure_tables_exist()
        session = pain_entry_database.create_session()
        location_list = []
        severity_list = []
        severity_list.append()
        pain_entry = PainEntry(time_stamp=datetime.now(), locations=location_list)
        MultipleScreenApp._pain_entry_severity(session, pain_entry, '', '')
        actual = session.query(PainEntryLocation).filter(PainEntryLocation.pain_location == '').one()
        self.assertEqual(actual.severity, 6)




if __name__ == '__main__':
    unittest.main()
