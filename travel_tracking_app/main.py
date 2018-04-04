from kivy.app import App
from sqlalchemy.exc import SQLAlchemyError
from sys import stderr

# noinspection PyUnresolvedReferences
from welcome_screen import WelcomeScreen
# noinspection PyUnresolvedReferences
from location_screen import LocationScreen
# noinspection PyUnresolvedReferences
from factor_screen import FactorScreen
# noinspection PyUnresolvedReferences
from facility_screen import FacilityScreen


class TravelTrackingApp(App):
    screens = ['welcome', 'location', 'factor', 'facility']

    def __init__(self, **kwargs):
        super(TravelTrackingApp, self).__init__(**kwargs)

    def open_next_screen(self):
        self.root.transition.direction = 'left'
        screen = self.root.current
        index = self.screens.index(screen)
        self.root.current = self.screens[index + 1]

    def open_previous_screen(self):
        self.root.transition.direction = 'right'
        screen = self.root.current
        index = self.screens.index(screen)
        self.root.current = self.screens[index - 1]

    def submit_form(self):
        try:
            self.root.ids.factor.ids.checkbox_1.state = 'normal'
            self.root.ids.factor.ids.checkbox_2.state = 'normal'
            self.root.ids.factor.ids.checkbox_3.state = 'normal'
            self.root.ids.factor.ids.checkbox_4.state = 'normal'
            self.root.ids.factor.ids.checkbox_5.state = 'normal'
            self.root.ids.factor.ids.checkbox_6.state = 'normal'
            self.root.current = self.screens[0]
        except SQLAlchemyError:
            print('Database connection not found. Please check connection to database.')

    def display_facilities(self, button):
        if str(button) == 'Columbus, NE':
            label = 'Urgent Care'
            self.root.ids.facility.ids.hospital_location.text = label
        if str(button) == 'Lincoln, NE':
            label = 'Pediatric Hospital, Community Hospital'
            self.root.ids.facility.ids.hospital_location.text = label
        if str(button) == 'Omaha, NE':
            label = 'Lakeside Hospital, UNMC'
            self.root.ids.facility.ids.hospital_location.text = label


def main():
    try:
        app = TravelTrackingApp()
        app.run()
    except SQLAlchemyError as exception:
        print('Problem loading the application. Try check connection to database.')
        print('Cause: {exception}'.format(exception=exception), file=stderr)

if __name__ == '__main__':
    main()
