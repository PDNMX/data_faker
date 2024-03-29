from faker import Faker
from faker.providers import ssn
import ast
import random
from timeit import default_timer as timer
from pathlib import Path
import pandas as pd
from dotmap import DotMap
from datetime import datetime
import random_data
import unicodedata
import re


fake = Faker('es_MX')
catalogs = {}
levels = [
    {
        "codigo": "EST",
        "valor": "Estatal"
    },
    {
        "codigo": "FED",
        "valor": "Federal"
    },
    {
        "codigo": "MUN",
        "valor": "Municipal"
    }
]


def load_catalogs(path_to_catalogs):
    global catalogs

    for file_path in Path(path_to_catalogs).glob('*.csv'):
        df = pd.read_csv(file_path)
        n = len(df.columns)
        name = Path(file_path).stem

        if n == 1:
            catalogs[name] = df[df.columns[0]].values
        else:
            catalogs[name] = df.to_dict('records')


def code(n=13):
    return fake.ean(length=n)


def date_time(args=None):
    if args is not None and len(args) > 0:
        if args[0] == 'now':
            return datetime.now().isoformat()
        if args[0] == 'birthday':
            return fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=100).strftime("%Y-%m-%d")

    return fake.date_time().isoformat()


def company(args=None):
    company_name = fake.company()
    if args is not None and len(args) > 0:
        if args[0] == 'clean':
            cleanName0 = unicodedata.normalize('NFD', company_name)
            cleanName1 = re.sub(r'-', ' ', cleanName0)
            cleanName2 = re.sub(r'[^\w\s]|_/g', '', cleanName1)
            cleanName3 = re.sub(r'\s+/g', ' ', cleanName2)
            company_name = cleanName3

            return company_name

    return company_name


def email():
    return fake.email()


def uri():
    return fake.uri()


def curp():
    return fake.curp()

def rfc(natural=True):
    return fake.rfc()

def ssn():
    return fake.ssn()

def building_number():
    return fake.building_number()

def fake_address():
    return random_data.get_address()

def bban():
    return fake.bban()

def year(args):
    if (args[0]) == "int":
        return int(fake.year())
    else:
        return fake.year()

def boolean():
    return fake.boolean()

def full_name():
    return fake.name()

def fake_dependent():
    return random_data.dependiente()

def lorem_text():
    return fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)

def custom_string(args):
    return args[0]

def currency_code():
    return fake.currency_code()


def first_name():
    return fake.first_name()


def last_name():
    return fake.last_name()


def country_code():
    return fake.country_code()


def country():
    return fake.country()


def phone_number():
    return fake.phone_number()


def postcode():
    return fake.postcode()


def street_name():
    return fake.street_name()


def from_list(args):
    return random.choice(ast.literal_eval(args[0]))


def street_type():
    return random.choice(['Calle', 'Bulevard'])


def from_catalog(args):
    name = args[0]
    return random.choice(catalogs[name]) if name in catalogs else None


def job():
    return fake.job()


def government_level():
    return random.choice(levels)


def in_range(args):
    if len(args) == 2:
        a = int(args[0])
        b = int(args[1])
        return random.randint(a, b)
    else:
        return 1


def constant(args):
    return args[0] if len(args) == 1 else 'NA'


def fake_int(args):
    return int(args[0]) if len(args) == 1 else 1


def from_seed(df, node, args):
    return df.get_seed(args[0]).get_value(node)


fakers = {
    'id': code,
    'date_time': date_time,
    'company': company,
    'email': email,
    'full_name': full_name,
    'uri': uri,
    'curp': curp,
    'rfc': rfc,
    'building_number': building_number,
    'fake_address': fake_address,
    'fake_dependent': fake_dependent,
    'custom_string': custom_string,
    'currency_code': currency_code,
    'last_name': last_name,
    'first_name': first_name,
    'country_code': country_code,
    'country': country,
    'phone_number': phone_number,
    'postcode': postcode,
    'street_name': street_name,
    'from_list': from_list,
    'from_catalog': from_catalog,
    'street_type': street_type,
    'job': job,
    'government_level': government_level,
    'in_range': in_range,
    'int': fake_int,
    'seed': from_seed,
    'year': year,
    'boolean': boolean,
    'lorem_text': lorem_text,
    'bban': bban
}


def fake_value(node, df=None):
    f = node.faker

    if not isinstance(f, str):
        raise TypeError('Faker "{}" is not a string.'.format(f))

    parts = f.split(':')
    f = parts[0]

    if f not in fakers:
        raise KeyError('Faker "{}" is not registered.'.format(f))

    if f == 'seed':
        return fakers[f](df, node, parts[1:])
    elif len(parts) > 1:
        f = parts[0]
        return fakers[f](parts[1:]) if f in fakers else 'fake'
    else:
        return fakers[f]() if f in fakers else 'fake'


class benchmark(object):

    def __init__(self, msg, fmt="%0.3g"):
        self.msg = msg
        self.fmt = fmt

    def __enter__(self):
        self.start = timer()
        return self

    def __exit__(self, *args):
        t = timer() - self.start
        print(("%s : " + self.fmt + " seconds") % (self.msg, t))
        self.time = t


class Seed:
    def __init__(self, name, props, state, next_state, initial_value, next_value):
        self.name = name
        self.props = DotMap(props)
        self.state = DotMap(state)
        self.next_state = next_state
        self.initial_value = initial_value
        self.value = None
        self.next_value = next_value
        self.df = None

    def get_value(self, node):
        if self.value is None:
            self.value = self.initial_value(self, node)
        else:
            self.value = self.next_value(self, node)

        self.state = DotMap(self.next_state(self))
        return self.value

    def reset(self, node):
        self.value = None
        return self.get_value(node)

    def set_df(self, df):
        self.df = df
