from kivy.app import App
from kivy.properties import NumericProperty, StringProperty
from sqlalchemy.exc import SQLAlchemyError
from sys import stderr

from kivy.logger import Logger

from openmrs import RESTConnection
from json import dumps

# noinspection PyUnresolvedReferences
from login import LoginScreen


class ProviderApp(App):
    def __init__(self, **kwargs):
        super(ProviderApp, self).__init__(**kwargs)
        self.openmrs_connection = None

    def user_login(self, username, password):
        self.openmrs_connection = RESTConnection('localhost', 8080, username, password)
        self.openmrs_connection.send_request()

    def on_login_success(self, _, response):
        print(dumps(response, indent=4, sort_keys=True))

    def on_login_failure(self, _, error):
        pass


    def load_openmrs_data(self):
        self.openmrs_connection.send_request('patient', None, self.on_openmrs_data_loaded,
                                             self.on_openmrs_data_not_loaded,
                                             self.on_openmrs_data_not_loaded(), '')

    def on_openmrs_data_loaded(self):
        pass

    def on_openmrs_data_not_loaded(self, _, error):
        Logger.error('RestApp: {error}'.format(error=error))


if __name__ == '__main__':
    try:
        app = ProviderApp()
        app.run()
    except SQLAlchemyError as exception:
        print('Initial database connection failed!', file=stderr)
        print('Cause: {exception}'.format(exception=exception), file=stderr)
        exit(1)
