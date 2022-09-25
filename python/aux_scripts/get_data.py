import os
import sys
import json
from datetime import datetime
import time
from faker import Faker
import csv
import random
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')


def curr_time():
    logging.debug("Called function {message}".format(message=sys._getframe(0).f_code.co_name))
    dt = datetime.now().strftime("%H:%M:%S.%f")[:-4]
    return dt


def generate_bulk(count, locale, json_file):
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
    logging.info("Called function {message}".format(message=sys._getframe(0).f_code.co_name))
    person = {}
    fake = Faker(locale)
    values_type = get_header_fields_name('fields', json_file)
    try:
        for i in range(0, count):
            person[i] = {}
            for k, v in values_type.items():
                person[i][k] = eval(v)
    except Exception as e:
        logging.error("Something wrong in function {message}. Error message {error}".format(message=sys._getframe(0).f_code.co_name, error=e))
    return person


def get_cvs_headers_name(json_file):
    logging.info("Called function {message}".format(message=sys._getframe(0).f_code.co_name))
    res = []
    with open(json_file) as json_file:
        data = json.load(json_file)
        for count, item in enumerate(data['fields'], start=1):
            keyIdx = f'key{count}'.format(count)
            dict_key = data['fields'][keyIdx]['name']
            res.append(f'{dict_key}'.format(dict_key))
    return res


def save_data_to_csv(*args):
    logging.info("Called function {message}".format(message=sys._getframe(0).f_code.co_name))
    headers = args[0]
    records = args[1]
    data = []
    for k, v in records.items():
        data.append(list(v.values()))
    with open('/tmp/persons.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f, delimiter =';')
        # write the headers
        writer.writerow(headers)
        # write the data
        writer.writerows(data)
    f.close()


def read_headers_json(headers_json_file_name, mode):
    logging.info("Called function {message}".format(message=sys._getframe(0).f_code.co_name))
    if mode == 'headers':
        res = []
    else:
        res = {}
    with open(headers_json_file_name) as json_file:
        data = json.load(json_file)
        if mode == 'headers':
            for count, item in enumerate(data['headers'], start=1):
                keyIdx = f'key{count}'.format(count)
                try:
                    res.append(data['headers'][keyIdx])
                except Exception as e:
                    logging.error("Json file is malformed. Error is: {message}".format(message=e))
        else:
            for count, item in enumerate(data['fields'], start=1):
                keyIdx = f'key{count}'.format(count)
                dict_key = data['fields'][keyIdx]['name']
                dict_value = data['fields'][keyIdx]['type']
                res[f'{dict_key}'.format(dict_key)] = dict_value.replace("'", "")
    return res


def get_header_fields_name(mode, json_file):
    logging.info("Called function {message}".format(message=sys._getframe(0).f_code.co_name))
    if mode == 'headers':
        try:
            res = read_headers_json(json_file, mode)
        except Exception as e:
            logging.error("Unable to execute get_header_fields_name. Error is: {message}".format(message=e))
            res = ['uuid', 'fio', 'phone', 'age', 'address', 'email']
    else:
        try:
            res = read_headers_json(json_file, mode)
        except Exception as e:
            logging.error("Unable to execute get_header_fields_name. Error is: {message}".format(message=e))
    return res


def read_env():
    logging.info("Called function {message}".format(message=sys._getframe(0).f_code.co_name))
    supportedLocale = ['ru_RU', 'pl_PL', 'en_US', 'en_GB', 'fr_FR', 'ja_JP']
    if os.getenv('LOCALE') in supportedLocale:
        LOCALE = os.getenv('LOCALE')
    else:
        LOCALE = 'ru_RU'
    logging.info("Env variable LOCALE set to: {message}".format(message=LOCALE))
    if os.getenv('PERSON_COUNT'):
        try:
            PERSON_COUNT = int(os.getenv('PERSON_COUNT'))
        except:
            PERSON_COUNT = 10
    else:
        PERSON_COUNT = 10
    logging.info("Env variable PERSON_COUNT set to: {message}".format(message=PERSON_COUNT))
    if os.getenv('OUTPUT_FILE_NAME'):
        OUTPUT_FILE_NAME = os.getenv('OUTPUT_FILE_NAME')
    else:
        OUTPUT_FILE_NAME = 'default.csv'
    logging.info("Env variable OUTPUT_FILE_NAME set to: {message}".format(message=OUTPUT_FILE_NAME))
    if os.getenv('JSON_TEMPLATE_FILE'):
        JSON_TEMPLATE_FILE = os.getenv('JSON_TEMPLATE_FILE')
    else:
        JSON_TEMPLATE_FILE = 'headers.json'
    logging.info("Env variable JSON_TEMPLATE_FILE set to: {message}".format(message=JSON_TEMPLATE_FILE))
    return (PERSON_COUNT, OUTPUT_FILE_NAME, JSON_TEMPLATE_FILE, LOCALE)


def actions(PERSON_COUNT, OUTPUT_FILE_NAME, JSON_TEMPLATE_FILE, LOCALE):
    logging.info("Called function {message}".format(message=sys._getframe(0).f_code.co_name))
    json_file = JSON_TEMPLATE_FILE
    persons = generate_bulk(PERSON_COUNT, LOCALE, json_file)
    headers = get_cvs_headers_name(json_file)
    save_data_to_csv(headers, persons)


def main():
    logging.info("Called function {message}".format(message=sys._getframe(0).f_code.co_name))
    PERSON_COUNT, OUTPUT_FILE_NAME, JSON_TEMPLATE_FILE, LOCALE = read_env()
    try:
        actions(PERSON_COUNT, OUTPUT_FILE_NAME, JSON_TEMPLATE_FILE, LOCALE)
    except Exception as e:
        logging.error("Unable to execute Actions. Error: {message}".format(message=e))


if __name__ == '__main__':
    logging.info("Called function {message}".format(message=sys._getframe(0).f_code.co_name))
    main()
