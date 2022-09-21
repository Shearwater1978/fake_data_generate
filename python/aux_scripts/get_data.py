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
import random


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


def read_headers_json(headers_json_file_name):
    print('%s -> Called function: >%s<' % (curr_time(), sys._getframe(0).f_code.co_name), file = sys.stdout)
    headers = ['uuid_json', 'fio_json', 'phone_json', 'age_json', 'address_json', 'email_json']
    with open(headers_json_file_name) as json_file:
        data = json.load(json_file)
        for count, item in enumerate(data['headers']):
            keyIdx = 'key' + count
            print(item)
            print('aaa')
            print('%s -> keyIdx: >%s<' % (curr_time(), keyIdx), file = sys.stdout)
    return headers


def get_header_fields_name():
    print('%s -> Called function: >%s<' % (curr_time(), sys._getframe(0).f_code.co_name), file = sys.stdout)
    headers_json_file_name = 'headers.json'
    try:
        os.path.isfile(headers_json_file_name)
        READ_HEADERS_JSON = True
        headers = read_headers_json(headers_json_file_name)
    except:
        headers = ['uuid', 'fio', 'phone', 'age', 'address', 'email']
    return headers
        

def read_env():
    if os.getenv('PERSON_COUNT'):
        try:
            PERSON_COUNT = int(os.getenv('PERSON_COUNT'))
        except:
            PERSON_COUNT = 10
    else:
        PERSON_COUNT = 10
    print('%s -> PERSON_COUNT set to: %s' % (curr_time(), PERSON_COUNT), file = sys.stdout)
    if os.getenv('NAME_OF_GENERATOR'):
        NAME_OF_GENERATOR = os.getenv('NAME_OF_GENERATOR')
    else:
        NAME_OF_GENERATOR = 'mimesis'
    print('%s -> NAME_OF_GENERATOR set to: %s' % (curr_time(), NAME_OF_GENERATOR), file = sys.stdout)
    if os.getenv('OUTPUT_FILE_NAME'):
        OUTPUT_FILE_NAME = os.getenv('OUTPUT_FILE_NAME')
    else:
        OUTPUT_FILE_NAME = 'default.csv'
    print('%s -> OUTPUT_FILE_NAME set to: %s' % (curr_time(), OUTPUT_FILE_NAME), file = sys.stdout)
    if os.getenv('USE_JSON_INPUT'):
        USE_JSON_INPUT = True
    else:
        USE_JSON_INPUT = False
    print('%s -> USE_JSON_INPUT set to: %s' % (curr_time(), USE_JSON_INPUT), file = sys.stdout)
    return(PERSON_COUNT, NAME_OF_GENERATOR, OUTPUT_FILE_NAME, USE_JSON_INPUT)


def actions(PERSON_COUNT, NAME_OF_GENERATOR, OUTPUT_FILE_NAME, USE_JSON_INPUT):
    persons = generate_bulk(PERSON_COUNT, NAME_OF_GENERATOR)
    print(get_header_fields_name())
    headers = ['uuid', 'fio', 'phone', 'age', 'address', 'email']
    save_data_to_csv(headers, persons)
    print('%s -> Output record(-s) saved to file' % curr_time(), file = sys.stdout)


def main():
    PERSON_COUNT, NAME_OF_GENERATOR, OUTPUT_FILE_NAME, USE_JSON_INPUT = read_env()
    print('%s -> Start work' % curr_time(), file = sys.stdout)
    print('%s -> Selected generator: %s' % (curr_time(), NAME_OF_GENERATOR), file = sys.stderr)
    try:
        print('%s -> Run main function' % curr_time(), file = sys.stdout)
        actions(PERSON_COUNT, NAME_OF_GENERATOR, OUTPUT_FILE_NAME, USE_JSON_INPUT)
    except Exception as e:
        print('%s -> Unable to execute Actions. Error: %s' % (curr_time(), e), file = sys.stdout)


if __name__ == '__main__':
    main()
