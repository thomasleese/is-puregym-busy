import os

import psycopg2
from puregym import PureGym


database_url = os.environ['DATABASE_URL']
email_address = os.environ['PUREGYM_EMAIL_ADDRESS']
pin = os.environ['PUREGYM_PIN']
name = os.environ['PUREGYM_NAME']

database = psycopg2.connect(database_url)

puregym = PureGym(email_address, pin)
number_of_people = puregym.my_gym.number_of_people

print(f'{name}: {number_of_people} people')

cursor = database.cursor()
cursor.execute("""
    INSERT INTO records(date, name, busyness) VALUES (NOW(), %s, %s)
""", (name, number_of_people))

database.commit()

cursor.close()
database.close()
