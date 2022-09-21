from mimesis.enums import Gender
from mimesis.locales import Locale
from mimesis.schema import Field, Schema
from mimesis.builtins import RussiaSpecProvider
from mimesis import Address
import os
import sys
import json
from datetime import datetime
import time
from faker import Faker
import csv


def curr_time():
    dt = datetime.now().strftime("%H:%M:%S.%f")[:-4]
    return(dt)


def generate_bulk(count, generator):
    if generator == 'mimesis':
        _ = Field(locale=Locale.RU)
        schema = Schema(schema=lambda: {
            "uuid": _("uuid"),
            "fio": _("full_name", gender=Gender.FEMALE, reverse = True) + ' ' + RussiaSpecProvider().patronymic(gender=Gender.FEMALE),
            "phone": _("person.telephone"),
            "age": _("person.age", minimum=18, maximum=118),
            "address": _("address.address"),
            "email": _("person.email", domains=["test.com"], key=str.lower)
        })
        res = schema.create(iterations=count)
    else:
        fake = Faker('ru_RU')
        res = [{
            "uuid": fake.uuid4(),
            "fio": fake.name(),
            "phone": fake.phone_number(),
            "age": random.randint(18,118),
            "address": fake.address(),
            "email": fake.email()} for x in range(count)]
    return(res)


def save_data_to_csv(*args):
    #headers = ['uuid', 'fio', 'phone', 'age', 'address', 'email']
    headers = args[0]
    records = args[1]
    data = []
    for item in range(0, len(records)):
        uuid = records[item]['uuid']
        fio = records[item]['fio']
        phone = records[item]['phone']
        age = records[item]['age']
        address = records[item]['address']
        email = records[item]['email']
        data.append(['%s' % uuid, '%s' % fio, '%s' % phone, '%s' % age, '%s' % address, '%s' % email])
    with open('/tmp/persons.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the headers
        writer.writerow(headers)
        # write the data
        writer.writerows(data)
    f.close()


def read_env():
    if os.getenv('PERSON_COUNT'):
        try:
            PERSON_COUNT = int(os.getenv('PERSON_COUNT'))
        except:
            print('%s -> PERSON_COUNT is set but value is not number. Used default value - 10' % curr_time(), file = sys.stdout)
            PERSON_COUNT = 10
    else:
        print('%s -> PERSON_COUNT not found as env varibale. Used default value - 10' % curr_time(), file = sys.stdout)
        PERSON_COUNT = 10
    if os.getenv('NAME_OF_GENERATOR'):
        NAME_OF_GENERATOR = os.getenv('NAME_OF_GENERATOR')
    else:
        NAME_OF_GENERATOR = 'mimesis'
    if os.getenv('OUTPUT_FILE_NAME'):
        try:
            OUTPUT_FILE_NAME = os.getenv('OUTPUT_FILE_NAME')
        except:
            OUTPUT_FILE_NAME = 'default.csv'
    return(PERSON_COUNT, NAME_OF_GENERATOR, OUTPUT_FILE_NAME)


def main():
    PERSON_COUNT, NAME_OF_GENERATOR, OUTPUT_FILE_NAME = read_env()
    print('%s -> Start work' % curr_time(), file = sys.stdout)
    print('%s -> Selected generator: %s' % (curr_time(), NAME_OF_GENERATOR), file = sys.stderr)
    try:
        print('%s -> Run main function' % curr_time(), file = sys.stdout)
        actions(PERSON_COUNT, NAME_OF_GENERATOR, OUTPUT_FILE_NAME)
    except Exception as e:
        print('%s -> Unable to execute Actions. Error: %s' % (curr_time(), e), file = sys.stdout)


if __name__ == '__main__':
    main()

