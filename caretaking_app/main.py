from kivy.app import App
from kivy.properties import StringProperty
from sqlalchemy.exc import SQLAlchemyError
from sys import stderr

# noinspection PyUnresolvedReferences
from login_screen import LoginScreen
# noinspection PyUnresolvedReferences
from input_screen import ObservationEntry
# noinspection PyUnresolvedReferences
from create_account import CreateAccount
# noinspection PyUnresolvedReferences
from caretaking_review_screen import ReviewScreen


class CareTakingApp(App):
    location = StringProperty('location type')
    activity = StringProperty('activity')
    appetite = StringProperty('appetite')
    date = StringProperty('date')
    city = StringProperty('city')
    weight = StringProperty('weight')
    temperature = StringProperty('temperature')
    patient = StringProperty('Select the patient visited')
    error = StringProperty('')

    def load(self):
        self.load_kv('caretaking.kv')

    def create_log(self):
        patient_id = self.root.ids.patient_spinner.text
        location = self.root.ids.location_type_spinner.text
        activity = self.root.ids.physical_activity.text
        appetite = self.root.ids.appetite.text
        app.error = self.root.ids.submit.text
        birth = self.root.ids.birthdate.text
        city = self.root.ids.address.text
        temp = self.root.ids.temp.text
        weight = self.root.ids.weight.text
        missing_field = 'You are missing one or many fields'
        if patient_id == 'Select the patient visited':
            app.error = missing_field
        if location == 'Select the location type of visit':
            app.error = missing_field
        if activity == 'Select value of Patient\'s physical activity':
            app.error == missing_field
        if appetite == 'Select value of Patient\'s appetite level':
            app.error == missing_field
        if birth == '':
            app.error == missing_field
        if city == '':
            app.error == missing_field
        if temp == '':
            app.error == missing_field
        if weight == '':
            app.error == missing_field
        else:
            app.error == 'Log Completed'
            self.root.transition.direction = 'left'
            self.root.current = 'review'

    def login_in(self):
        self.root.transition.direction = 'left'
        self.root.current = 'observation'

    def create_account(self):
        self.root.transition.direction = 'left'
        self.root.current = 'create account'

    def back_to_login(self):
        self.root.transition.direction = 'left'
        self.root.current = 'login'


if __name__ == '__main__':
    try:
        app = CareTakingApp()
        app.run()
    except SQLAlchemyError as exception:
        print('Initial database connection failed!', file=stderr)
        print('Cause: {exception}'.format(exception=exception), file=stderr)
        exit(1)
