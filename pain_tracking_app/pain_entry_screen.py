from tkinter import Label

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


Builder.load_file('pain_entry.kv')


class PainEntryScreen(Screen):

    def save_pain(self):
        pass
