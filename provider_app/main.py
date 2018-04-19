from kivy.app import App
from kivy.properties import NumericProperty, StringProperty
from sqlalchemy.exc import SQLAlchemyError
from sys import stderr

from kivy.logger import Logger

from openmrs import RESTConnection
from json import dumps

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
            self.load_openmrs_data()
        else:
            self.root.ids.login.ids.error_message.text = 'Username and/or password is incorrect. Please try again.'

    def on_login_failure(self):
        self.root.ids.login.ids.error_message.text = 'Failed to Login.'

    def on_login_error(self, _, error):
        self.root.ids.login.ids.error_message.text = 'Check connection to OpenMRS'
        Logger.error('RestApp: {error}'.format(error=error))

    def load_patient(self):

        pass

    def load_openmrs_data(self):
        self.openmrs_connection.send_request('patient', None, self.on_openmrs_data_loaded,
                                             self.on_openmrs_data_not_loaded,
                                             self.on_openmrs_data_error, 'v=full')

    def on_openmrs_data_loaded(self, _, response):
        print(dumps(response, indent=4, sort_keys=True))

    def on_openmrs_data_not_loaded(self, _, error):
        self.root.ids.select_patient.ids.failure_message.text = 'Failed to load patient data. Retest OpenMRS connection.'

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
