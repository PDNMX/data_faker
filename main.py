from datafaker import DataFaker
import json
from util import benchmark, Seed, code
import copy
import dateparser
from dateutil.relativedelta import relativedelta


if __name__ == '__main__':
    path_to_file = './oas/declaraciones_with_faker.json'
    path_to_schema = '#/components/schemas/Declaraciones/properties/results'
    path_to_catalogs = './catalogs'
    n = 3

    document_id_seed = Seed(
        name='document_id',
        props={'n': n},
        state={'count': 0},
        next_state=lambda seed: {'count': seed.state.count + 1},
        initial_value=lambda seed, node: code(),
        next_value=lambda seed, node: seed.value if seed.state.count % seed.props.n != 0 else seed.reset(node)
    )

    def next_personal_info(seed, node):
        if seed.state.count % seed.props.n != 0:
            dt = seed.value['informacion_general']['fecha_declaracion']
            dt = (dateparser.parse(dt) + relativedelta(months=12)).isoformat()
            data = copy.deepcopy(seed.value.copy())
            data['informacion_general']['fecha_declaracion'] = dt
            return data
        else:
            return seed.reset(node)

    personal_info = Seed(
        name='informacion_personal',
        props={'n': n},
        state={'count': 0},
        next_state=lambda seed: {'count': seed.state.count + 1},
        initial_value=lambda seed, node: seed.df.fake_node(node),
        next_value=next_personal_info
    )

    with benchmark('data faker'):
        data_faker = DataFaker(path_to_file, path_to_schema, path_to_catalogs)
        data_faker.add_seed(document_id_seed)
        data_faker.add_seed(personal_info)
        fake_data = data_faker.fake()
        # print(json.dumps(fake_data, indent=2))
        DataFaker.save(
            fake_data,
            'f_declaraciones',
            'db',
            dict(db='oas', host='localhost', port=27017)
        )
