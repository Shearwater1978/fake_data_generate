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


def generate_bulk(count, locale):
    """
        List of explicitly supported locales:
            - ru_RU
            - pl_PL
            - en_US
            - en_GB
            - fr_FR
            - ja_JP
        Another locale must be checked by user. Full list of available locales 
        can be reached with URL: https://faker.readthedocs.io/en/master/locales.html
        If needed locale is working without error, you should update list supportedLocale to be added locale in supported
    """
    print('%s -> Called function: >%s_new<' % (curr_time(), sys._getframe(0).f_code.co_name), file = sys.stdout)  
    person = {}
    fake = Faker(locale)
    values_type = get_header_fields_name('fields')
    for i in range(0, count):
        person[i] = {}
        for k, v in values_type.items():
            person[i][k] = eval(v)
    return person


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


def read_headers_json(headers_json_file_name, mode):
    print('%s -> Called function: >%s< in mode: >%s<' % (curr_time(), sys._getframe(0).f_code.co_name, mode), file = sys.stdout)  
    if mode == 'headers':
        res = []
    elif mode == 'fields':
        res = {}
    else:
        print('%s -> Wrong mode. Error message: %s. Terminating script' % (curr_time(), e), file = sys.stdout)
    with open(headers_json_file_name) as json_file:
        data = json.load(json_file)
        if mode == 'headers':
            for count, item in enumerate(data['headers'], start=1):
                keyIdx = f'key{count}'.format(count)
                try:
                    res.append(data['headers'][keyIdx])
                except Exception as e:
                    print('%s -> Json file is malformed. Error message: %s. Terminating script' % (curr_time(), e), file = sys.stdout)
        else:
            print('%s -> Triggered ELSE section' % (curr_time()), file = sys.stdout)
            for count, item in enumerate(data['fields'], start=1):
                keyIdx = f'key{count}'.format(count)
                dict_key = data['fields'][keyIdx]['name']
                dict_value = data['fields'][keyIdx]['type']
                res[f'{dict_key}'.format(dict_key)] = dict_value.replace("'", "")
    return res


def get_header_fields_name(mode):
    print('%s -> Called function: >%s<' % (curr_time(), sys._getframe(0).f_code.co_name), file = sys.stdout)
    headers_json_file_name = 'headers.json'
    if mode == 'headers':
        print('%s -> Called mode: >%s<' % (curr_time(), mode), file = sys.stdout)
        try:
            os.path.isfile(headers_json_file_name)
            READ_HEADERS_JSON = True
            res = read_headers_json(headers_json_file_name, mode)
        except Exception as e:
            print('%s -> Unable to execute Actions in mode: %s. Error: %s' % (curr_time(), mode, e), file = sys.stdout)
            res = ['uuid', 'fio', 'phone', 'age', 'address', 'email']
    else:
        print('%s -> Called mode: >%s<' % (curr_time(), mode), file = sys.stdout)
        try:
            os.path.isfile(headers_json_file_name)
            READ_HEADERS_JSON = True
            res = read_headers_json(headers_json_file_name, mode)
        except Exception as e:
            print('%s -> Unable to execute Actions in mode: %s. Error: %s' % (curr_time(), mode, e), file = sys.stdout)
    return res


def read_env():
    supportedLocale = [ 'ru_RU', 'pl_PL', 'en_US', 'en_GB', 'fr_FR', 'ja_JP' ]
    print('%s -> Called function: >%s<' % (curr_time(), sys._getframe(0).f_code.co_name), file = sys.stdout)
    if os.getenv('LOCALE') in supportedLocale:
        LOCALE = os.getenv('LOCALE')
    else:
        LOCALE = 'ru_RU'
    print('%s -> LOCALE set to: %s' % (curr_time(), LOCALE), file = sys.stdout)
    if os.getenv('PERSON_COUNT'):
        try:
            PERSON_COUNT = int(os.getenv('PERSON_COUNT'))
        except:
            PERSON_COUNT = 10
    else:
        PERSON_COUNT = 10
    print('%s -> PERSON_COUNT set to: %s' % (curr_time(), PERSON_COUNT), file = sys.stdout)
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
    return(PERSON_COUNT, OUTPUT_FILE_NAME, USE_JSON_INPUT, LOCALE)


def actions(PERSON_COUNT, OUTPUT_FILE_NAME, USE_JSON_INPUT, LOCALE):
    persons = generate_bulk(PERSON_COUNT, LOCALE)
    # headers = get_header_fields_name('headers')
    # values = get_header_fields_name('values')
    # save_data_to_csv(headers, persons)
    print(persons)
    print('%s -> Output record(-s) saved to file' % curr_time(), file = sys.stdout)


def main():
    PERSON_COUNT, OUTPUT_FILE_NAME, USE_JSON_INPUT, LOCALE = read_env()
    print('%s -> Start work' % curr_time(), file = sys.stdout)
    try:
        print('%s -> Run main function' % curr_time(), file = sys.stdout)
        actions(PERSON_COUNT, OUTPUT_FILE_NAME, USE_JSON_INPUT, LOCALE)
    except Exception as e:
        print('%s -> Unable to execute Actions. Error: %s' % (curr_time(), e), file = sys.stdout)


if __name__ == '__main__':
    main()
