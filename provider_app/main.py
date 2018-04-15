from kivy.app import App
from kivy.properties import NumericProperty, StringProperty
from sqlalchemy.exc import SQLAlchemyError
from sys import stderr


class ProviderApp(App):
    pass


if __name__ == '__main__':
    try:
        app = ProviderApp()
        app.run()
    except SQLAlchemyError as exception:
        print('Initial database connection failed!', file=stderr)
        print('Cause: {exception}'.format(exception=exception), file=stderr)
        exit(1)
