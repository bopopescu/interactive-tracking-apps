import unittest
from datetime import datetime
# noinspection PyUnresolvedReferences
from caretaking_app import main
# noinspection PyUnresolvedReferences
from caretaking_app.caretaking import CareTakingDatabase
# noinspection PyUnresolvedReferences
from caretaking import CareTakingDatabase, Patient, CareLog, Observation





class MyTestCase(unittest.TestCase):
    def test_insert_medication(self):
        url = CareTakingDatabase.construct_in_memory_url()
        medication_entry_database = CareTakingDatabase(url)
        medication_entry_database.ensure_tables_exist()
        session = medication_entry_database.create_session()
        jimmy_fallon = Patient(name='Jimmy Fallon')
        care_log = CareLog()
        jimmy_obs = Observation(patient= jimmy_fallon,log = care_log,location='Patient Home', activity='5-Very Active', appetite = '5-Very Healthy', birthdate='05/04/1998', city ='Omaha', weight='120', temperature='50', date_time=datetime(2018,4,12,20,11,12,13))



if __name__ == '__main__':
    unittest.main()
