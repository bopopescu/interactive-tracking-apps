# -*- coding: utf-8; -*-

from sys import stderr
from sqlalchemy.exc import SQLAlchemyError
from pain_entries import MedicationEntry,MedicationEntryDosage,PainEntryLocation,PainLocation,PainMedicationDatabase,\
    Medicine,PainEntry
import datetime


def add_starter_data(session):
    # beverage_menu = Menu(name='Beverage')
    # food_menu = Menu(name='Food')
    # orange_juice = Item(menu=beverage_menu, name='Orange Juice', price=149)
    # short_stack = Item(menu=food_menu, name='Pancakes', price=399)
    # regular_pancakes = Item(menu=food_menu, name='Pancakes', price=499)
    # first_order = Order(order_items=[OrderItem(item=orange_juice, amount=2)])

    arm_location = PainLocation(body_location = 'Arm')
    leg_location = PainLocation(body_location = 'Leg')
    head_location = PainLocation(body_location = 'Head')
    stomach_location = PainLocation(body_location = 'Stomach')

    Acetyl = Medicine(medicine_type = 'Acetylsalicylic (mg)')
    paracetamol = Medicine(medicine_type = 'Paracetamol (ml)')
    Ibuprofen = Medicine(medicine_type = 'Ibuprofen (mg)')

    session.add(leg_location)
    session.add(arm_location)
    session.add(head_location)
    session.add(stomach_location)
    session.add(Acetyl)
    session.add(paracetamol)
    session.add(Ibuprofen)


def main():
    try:
        url = PainMedicationDatabase.construct_mysql_url('localhost', 3306, 'pain_tracking', 'root', 'cse')
        diner_database = PainMedicationDatabase(url)
        diner_database.ensure_tables_exist()
        print('Tables created.')
        session = diner_database.create_session()
        add_starter_data(session)
        session.commit()
        print('Records created.')
    except SQLAlchemyError as exception:
        print('Database setup failed!', file=stderr)
        print('Cause: {exception}'.format(exception=exception), file=stderr)
        exit(1)


if __name__ == '__main__':
    main()
