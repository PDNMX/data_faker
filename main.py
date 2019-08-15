import argparse
from datafaker import DataFaker
import json
from util import benchmark, Seed, code
import copy
import dateparser
from dateutil.relativedelta import relativedelta
import dns
import os
from pyfiscal import generate
from datetime import datetime
from unidecode import unidecode

parser = argparse.ArgumentParser(description='Data Faker')

parser.add_argument('-s', '--sys', default=1, type=int,
                    help='System number', choices=[1, 2, 3])
parser.add_argument('-n', '--samples', default=1,
                    type=int, help='Number of samples')
parser.add_argument('-y', '--years', default=2,
                    type=int, help='Number of years for declarant')
args = parser.parse_args()

sys_number = args.sys
number_of_samples = args.samples
years = args.years

dbname = os.environ.get('DATAFAKE_MONGO_DB_NAME', 'oas')
host = os.environ.get('DATAFAKE_MONGO_HOST', 'localhost')
port = os.environ.get('DATAFAKE_MONGO_PORT', 27017)
user = os.environ.get('DATAFAKE_MONGO_USER', None)
password = os.environ.get('DATAFAKE_MONGO_PASS', None)

if __name__ == '__main__':

    path_to_catalogs = './catalogs'
    n = years

    if sys_number == 1:
        path_to_file = './oas/declaraciones_with_faker.json'
        path_to_schema = '#/components/schemas/Declaraciones/properties/results'
        document_id_seed = Seed(
            name='document_id',
            props={'n': n},
            state={'count': 0},
            next_state=lambda seed: {'count': seed.state.count + 1},
            initial_value=lambda seed, node: code(),
            next_value=lambda seed, node: seed.value if seed.state.count % seed.props.n != 0 else seed.reset(node)
        )
        document_samples = Seed(
            name='samples',
            props={'n': years},
            state={'count': 0},
            next_state=lambda seed: {'count': seed.state.count + 1},
            initial_value=lambda seed, node: years,
            next_value=lambda seed, node: seed.value
        )

        def next_personal_info(seed, node):
            if seed.state.count % seed.props.n != 0:
                # Update  year
                dt = seed.value['informacion_general']['fecha_declaracion']
                dt = (dateparser.parse(dt) + relativedelta(months=12)).isoformat()
                data = copy.deepcopy(seed.value.copy())
                data['informacion_general']['fecha_declaracion'] = dt
                return data
            else:
                return seed.reset(node)

        def get_initial_pi(seed, node):
            data = seed.df.fake_node(node)
            # validate CURP and RFC
            kwargs = {
                "complete_name": unidecode(data['informacion_general']['nombres']),
                "last_name": unidecode(data['informacion_general']['primer_apellido']),
                "mother_last_name": unidecode(data['informacion_general']['segundo_apellido']),
                "birth_date": (
                    datetime.strptime(data['informacion_general']['fecha_nacimiento'], '%Y-%m-%d')).strftime(
                    '%d-%m-%Y'),
                "gender": "H",
                "city": data['informacion_general']['entidad_federativa_nacimiento']['nom_agee'],
                "state_code": str(data['informacion_general']['entidad_federativa_nacimiento']['cve_agee'])
            }
            # CURP and RFC Fix
            data['informacion_general']['curp'] = generate.GenerateCURP(**kwargs).data
            # RFC
            data['informacion_general']['rfc'] = generate.GenerateRFC(**kwargs).data
            return data

        for x in range(0, number_of_samples):
            personal_info = Seed(
                name='informacion_personal',
                props={'n': n},
                state={'count': 0},
                next_state=lambda seed: {'count': seed.state.count + 1},
                initial_value=get_initial_pi,
                next_value=next_personal_info
            )
            with benchmark('data faker'):
                data_faker = DataFaker(path_to_file, path_to_schema, path_to_catalogs)
                data_faker.add_seed(document_id_seed)
                data_faker.add_seed(document_samples)
                data_faker.add_seed(personal_info)
                fake_data = data_faker.fake()
                # print(json.dumps(fake_data, indent=2))
                print("send_save_" + str(x))
                DataFaker.save(
                    fake_data,
                    's1',
                    'db',
                    dict(db=dbname, host=host, port=port, user=user, password=password)
                )

    elif sys_number == 2:
        path_to_file = './oas/OAS_API_servidores_intervienen_contrataciones_with_faker.json'
        path_to_schema = '#/components/schemas/spic/properties/results'

        document_id_seed = Seed(
            name='document_id',
            props={'n': n},
            state={'count': 0},
            next_state=lambda seed: {'count': seed.state.count + 1},
            initial_value=lambda seed, node: code(),
            next_value=lambda seed, node: seed.value if seed.state.count % seed.props.n != 0 else seed.reset(node)
        )

        document_samples = Seed(
            name='samples',
            props={'n': number_of_samples},
            state={'count': 0},
            next_state=lambda seed: {'count': seed.state.count + 1},
            initial_value=lambda seed, node: years,
            next_value=lambda seed, node: seed.value
        )


        def next_document_info(seed, node):
            if seed.state.count % seed.props.n != 0:
                # Update  year
                dt = seed.value['fecha_captura']
                dt = (dateparser.parse(dt) + relativedelta(months=12)).isoformat()
                data = copy.deepcopy(seed.value.copy())
                data['fecha_captura'] = dt
                return data
            else:
                return seed.reset(node)


        def get_initial_document(seed, node):
            data = seed.df.fake_node(node)
            return data


        for x in range(0, number_of_samples):
            document_info = Seed(
                name='servidores',
                props={'n': n},
                state={'count': 0},
                next_state=lambda seed: {'count': seed.state.count + 1},
                initial_value=get_initial_document,
                next_value=next_document_info
            )
            with benchmark('data faker'):
                data_faker = DataFaker(path_to_file, path_to_schema, path_to_catalogs)
                data_faker.add_seed(document_id_seed)
                data_faker.add_seed(document_samples)
                data_faker.add_seed(document_info)
                fake_data = data_faker.fake()
                # del fake_data['id']
                # print(json.dumps(fake_data, indent=2))
                print("send_save_" + str(x))
                DataFaker.save(
                    fake_data,
                    's2',
                    'db',
                    dict(db=dbname, host=host, port=port, user=user, password=password)
                )
    elif sys_number == 3:
        path_to_file = ''
        path_to_schema = ''
        print("work in progress")
