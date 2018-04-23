from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from sqlalchemy.exc import SQLAlchemyError
from sys import stderr
from kivy.logger import Logger
from openmrs import RESTConnection
from json import dumps
from database import CombinedDatabase, PainLocation, PainEntryLocation, PainEntry, Medicine, MedicationEntry, \
    MedicationEntryDosage, Patient, User, Observation

# noinspection PyUnresolvedReferences
from login import LoginScreen
# noinspection PyUnresolvedReferences
from select_patient import PatientScreen
# noinspection PyUnresolvedReferences
from review import ReviewScreen


class ProviderApp(App):
    username = StringProperty()
    password = StringProperty()

    def __init__(self, **kwargs):
        super(ProviderApp, self).__init__(**kwargs)
        self.openmrs_connection = None
        url = CombinedDatabase.construct_mysql_url('mysql.poetical-science.org', 3306, 'soft161_team_6', 'soft161_team_6', 'chromosome+differentiates<')
        self.provider_database = CombinedDatabase(url)
        self.session = self.provider_database.create_session()

    def user_login(self, username, password):
        self.openmrs_connection = RESTConnection('localhost', 8080, username, password)
        self.openmrs_connection.send_request('session', None, self.on_login_success, self.on_login_failure, self.on_login_error, '')

    def user_logout(self):
        self.root.transition.direction = 'right'
        self.root.current = 'login'
        self.root.ids.select_patient.ids.patients.clear_widgets()

    def select_patient(self):
        self.root.transition.direction = 'right'
        self.root.current = 'select_patient'

    def on_login_success(self, _, response):
        if response.get('authenticated'):
            self.root.transition.direction = 'left'
            self.root.current = 'select_patient'
            self.root.ids.login.ids.password.text = ''
            self.root.ids.login.ids.error_message.text = ''
            self.load_patients()
        else:
            self.root.ids.login.ids.error_message.text = 'Username and/or password is incorrect. Please try again.'

    def on_login_failure(self):
        self.root.ids.login.ids.error_message.text = 'Failed to Login.'

    def on_login_error(self, _, error):
        self.root.ids.login.ids.error_message.text = 'Check connection to OpenMRS'
        Logger.error('RestApp: {error}'.format(error=error))

    def load_patients(self):
        patients = self.session.query(Patient).all()
        for x in range(len(patients)):
            new_patient = Button(text='{name}'.format(name=patients[x].name),
                                 on_press=lambda y: self.load_openmrs_data(patients[x].open_mrs_id))
            self.root.ids.select_patient.ids.patients.add_widget(new_patient)

    def load_openmrs_data(self, openmrs_id):
        self.root.transition.direction = 'left'
        self.root.current = 'review'
        self.root.ids.review.ids.data.clear_widgets()
        patient = self.session.query(Patient).filter(Patient.open_mrs_id == openmrs_id).one()
        self.load_database_data(patient.patient_id)
        self.openmrs_connection.send_request('patient', None, self.on_openmrs_data_loaded,
                                             self.on_openmrs_data_not_loaded,
                                             self.on_openmrs_data_error, 'q={user_id}&v=full'.format(user_id=openmrs_id))

    def on_openmrs_data_loaded(self, _, response):
        for result in response['results']:
            self.openmrs_connection.send_request('encounter', None, self.on_visit_data_loaded,
                                                 self.on_openmrs_data_not_loaded, self.on_openmrs_data_error,
                                                 'q={uuid}&v=full'.format(uuid=result['uuid']))

    def on_visit_data_loaded(self, _, response):
        #print(dumps(response, indent=4, sort_keys=True))
        visit_times = self.root.ids.review.ids.visit_times
        encounters = self.root.ids.review.ids.visit_encounters
        # for result in response['results']:
        #     visit_times.add_widget(Label(text='{encounterDatetime}'.format(encounterDatetime=result['encounterDatetime'])))

    def load_database_data(self, patient_id):
        observation = self.session.query(Observation).filter(Observation.patient_id == patient_id).one()
        location = observation.location
        activity = observation.activity
        appetite = observation.appetite
        weight = observation.weight
        temperature = observation.temperature
        print(temperature)
        self.root.ids.review.ids.database_entries.add_widget(Label(text='{location}'.format(location=location)))
        self.root.ids.review.ids.database_entries.add_widget(Label(text='{activity}'.format(activity=activity)))
        self.root.ids.review.ids.database_entries.add_widget(Label(text='{appetite}'.format(appetite=appetite)))
        self.root.ids.review.ids.database_entries.add_widget(Label(text='{weight}'.format(weight=weight)))
        self.root.ids.review.ids.database_entries.add_widget(Label(text='{temperature}'.format(temperature=temperature)))

    def on_openmrs_data_not_loaded(self, _, error):
        self.root.ids.select_patient.ids.failure_message.text = 'Failed to load patient data. Retest OpenMRS connection.'
        Logger.error('RestApp: {error}'.format(error=error))

    def on_openmrs_data_error(self, _, error):
        Logger.error('RestApp: {error}'.format(error=error))


if __name__ == '__main__':
    try:
        app = ProviderApp()
        app.run()
    except SQLAlchemyError as exception:
        print('Initial database connection failed!', file=stderr)
        print('Cause: {exception}'.format(exception=exception), file=stderr)
        exit(1)
