from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.label import Label
from sqlalchemy.exc import SQLAlchemyError
from sys import stderr
# noinspection PyUnresolvedReferences
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.sql.functions import user
from database import Patient, User, Observation, CombinedDatabase
from login_screen import LoginScreen
# noinspection PyUnresolvedReferences
from input_screen import ObservationEntry
# noinspection PyUnresolvedReferences
from create_account import CreateAccount
# noinspection PyUnresolvedReferences
from caretaking_review_screen import ReviewScreen
# noinspection PyUnresolvedReferences
from kivy.storage.jsonstore import JsonStore


class CareTakingApp(App):

    store = JsonStore('users.json')
    location = StringProperty('location type')
    activity = StringProperty('activity')
    appetite = StringProperty('appetite')
    date = StringProperty('date')
    city = StringProperty('city')
    weight = StringProperty('weight')
    temp = StringProperty('temperature')
    patient = StringProperty('Select the patient visited')
    error = StringProperty('')
    patient_id = StringProperty('')
    birth = StringProperty('')
    account_surname = StringProperty('')
    account_given_name = StringProperty('')
    account_patient_id = StringProperty('')
    missing_field = StringProperty('')
    username = StringProperty('')
    verification = StringProperty('')
    failed = StringProperty('')
    account_verification = StringProperty('')

    def __init__(self, **kwargs):
        super(CareTakingApp, self).__init__(**kwargs)
        url = CombinedDatabase.construct_mysql_url('mysql.poetical-science.org', 3306, 'soft161_team_6', 'soft161_team_6', 'chromosome+differentiates<')
        self.care_tracking_database = CombinedDatabase(url)
        self.session = self.care_tracking_database.create_session()

    def load(self):
        self.load_kv('caretaking.kv')

    #create log checks if the user has inputed vaild values and verifies their confirmation
    def create_log(self):
        self.patient_id = self.root.ids.observation.ids.patient_spinner.text
        self.location = self.root.ids.observation.ids.location_type_spinner.text
        self.activity = self.root.ids.observation.ids.physical_activity.text
        self.appetite = self.root.ids.observation.ids.appetite.text
        self.error = self.root.ids.observation.ids.submit.text
        self.birth = self.root.ids.observation.ids.birthdate.text
        self.city = self.root.ids.observation.ids.address.text
        self.temp = self.root.ids.observation.ids.temp.text
        self.weight = self.root.ids.observation.ids.weight.text
        self.missing_field = 'You are missing one or many fields'
        self.user_id = '10002T'

        if self.patient_id == '':
            self.error = self.missing_field
        if self.location == 'Select the location type of visit':
            self.error = self.missing_field
        if self.activity == "Select value of Patient\'s physical activity":
            self.error = self.missing_field
        if self.appetite == "Select value of Patient\'s appetite level":
            self.error = self.missing_field
        if self.birth == '':
            self.error = self.missing_field
        if self.city == '':
            self.error = self.missing_field
        if self.temp == '':
            self.error = self.missing_field
        if self.weight == '':
            self.error = self.missing_field
        else:
            self.review_screen()
            self.error = 'Log Completed'
            self.root.transition.direction = 'left'
            self.root.current = 'review'

        self.get_data()

    def main_menu(self):
        self.root.transition.direction = 'left'
        self.root.current = 'login'

    def login_in(self):

        self.username = ('{g} {p}'.format(g=self.root.ids.create_account.ids.given_name.text, p = self.root.ids.create_account.ids.patient_id.text))
        self.account_verification = self.root.ids.login.ids.account_verification.text
        if self.root.ids.login.ids.accounts.text == "Select your account":
            self.account_verification = 'You must select an account to login or create an account'
        else:

         self.username = ('{g} {p}'.format(g=self.root.ids.create_account.ids.given_name.text, p = self.root.ids.create_account.ids.patient_id.text))
         self.account_verification = self.root.ids.login.ids.account_verification.text


    def create_account(self):
        self.root.transition.direction = 'left'
        self.root.current = 'create account'

    # back to login makes sure when the user creates an account that they have inputted
    # valid information
    def back_to_login(self):
        self.account_surname = self.root.ids.create_account.ids.surname.text
        self.account_given_name = self.root.ids.create_account.ids.given_name.text
        self.account_patient_id = self.root.ids.create_account.ids.patient_id.text
        self.username = ('{g} {p}'.format(g=self.root.ids.create_account.ids.given_name.text, p = self.root.ids.create_account.ids.patient_id.text))
        self.verification = self.root.ids.create_account.ids.account_verification.text
        self.missing_field = 'You are missing one or many fields'
        if self.account_surname == '' or self.account_given_name == '' or self.account_patient_id == '':
            self.verification = self.missing_field
        else:
            self.root.transition.direction = 'left'
            self.root.current = 'login'

    # submit entry queries each observation, patient and user into the database
    def _submit_entry(self):
        user = User(surname = self.root.ids.observation.ids.patient_spinner.text, given_name=self.root.ids.observation.ids.patient_spinner.text)
        patient = Patient(name = self.root.ids.observation.ids.patient_spinner.text, user_id = user.user_id)
        observation = Observation(location = self.root.ids.observation.ids.location_type_spinner.text,\
                                  activity = self.root.ids.observation.ids.physical_activity.text,\
                                  appetite = self.root.ids.observation.ids.appetite.text,\
                                  birth_date = self.root.ids.observation.ids.birthdate.text,\
                                  city = self.root.ids.observation.ids.address.text,\
                                  temperature = self.root.ids.observation.ids.temp.text,\
                                  weight = self.root.ids.observation.ids.address.text,\
                                  patient = patient)
        try:
            self.session.add(user)
            self.session.add(patient)
            self.session.add(observation)
            self.session.commit()
            print('Successful')
        except SQLAlchemyError as exception:
            print('Database setup failed!', file=stderr)
            print('Cause: {exception}'.format(exception=exception), file=stderr)
        except MultipleResultsFound:
            print('Can not create, multiple results found')
        except NoResultFound:
            print('No results found')

    def get_data(self):
        jon = self.session.query(Patient).filter(Patient.name == 'Jon Smith').one()
        jon.user_id = '10001V'
        self.session.add(jon)
        self.session.commit()
        patients = self.session.query(Patient).filter(Patient.user_id == self.user_id).all()

    def _load_state(self):
        try:
            users = []
            self.root.ids.login.ids.accounts.values = list(self.store.keys())

            print(list(self.store.keys()))
        except KeyError:
            pass

    def _save_state(self):
        self.store.put(str(self.account_patient_id), given_name = self.account_given_name)

    def on_start(self):
        self._load_state()

    def on_pause(self):
        self._save_state()
        return True

    def on_stop(self):
        self._save_state()

    def review_screen(self):
        container = self.root.ids.review.ids.patient_records

        #user_list = list(self.store.keys())
        #patient_list = []
        # for user in user_list:
        #     patient_list.append(self.session.query(Patient).filter(Patient.user_id == user).all())

        for observation in self.session.query(Observation).order_by(Observation.date_time).all():
            container.add_widget(Label(text = observation.city))


if __name__ == '__main__':
    try:
        app = CareTakingApp()
        app.run()
    except SQLAlchemyError as exception:
        print('Initial database connection failed!', file=stderr)
        print('Cause: {exception}'.format(exception=exception), file=stderr)
        exit(1)

