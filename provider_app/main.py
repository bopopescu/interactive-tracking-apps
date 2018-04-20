from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.button import Button
from sqlalchemy.exc import SQLAlchemyError
from sys import stderr
from kivy.logger import Logger
from openmrs import RESTConnection
from json import dumps
from database import CombinedDatabase, PainLocation, PainEntryLocation, PainEntry, Medicine, MedicationEntry, \
    MedicationEntryDosage, Patient

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
        for patient in patients:
            new_patient = Button(text=patient.name, on_press=lambda x: self.load_openmrs_data(patient.name))
            self.root.ids.select_patient.ids.patients.add_widget(new_patient)

    def load_openmrs_data(self, name):
        self.root.transition.direction = 'left'
        self.root.current = 'review'
        self.openmrs_connection.send_request('patient', None, self.on_openmrs_data_loaded,
                                             self.on_openmrs_data_not_loaded,
                                             self.on_openmrs_data_error, 'q=name&v=full')

    def on_openmrs_data_loaded(self, _, response):
        print(response)
        for patient in response['results']:
            pass

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
