import json
from dotmap import DotMap
from util import fake_value, load_catalogs
from pymongo import MongoClient


class DataFaker:
    STRING = 'string'
    OBJECT = 'object'
    ARRAY = 'array'

    def __init__(self, path_to_file, path_to_schema, path_to_catalogs):
        self.path_to_file = path_to_file
        self.path_to_schema = path_to_schema
        self.path_to_catalogs = path_to_catalogs
        self.root = None
        self.schema = None
        self.read()
        self.seeds = {}
        self.client = MongoClient(host='localhost', port=27017)
        load_catalogs(self.path_to_catalogs)

    @staticmethod
    def __get_paths(path_str):
        return path_str.replace('#/', '').split('/')

    def read(self):
        with open(self.path_to_file) as json_file:
            self.root = json.load(json_file)

        if self.root is not None:
            self.schema = self.root
            paths = self.__get_paths(self.path_to_schema)

            for path in paths:
                self.schema = DotMap(self.schema[path])

    def __get_node(self, path_to_node):
        node = self.root
        paths = self.__get_paths(path_to_node)

        for path in paths:
            node = DotMap(node[path])

        return DotMap(node.copy())

    def __init_property(self, p):
        if '$ref' in p:
            faker = p.faker if 'faker' in p else None
            p = self.__get_node(p['$ref'])

            if faker is not None:
                p['faker'] = faker

        if p.type == self.OBJECT:
            return self.__init_properties(p)
        elif p.type == self.ARRAY and 'items' in p:
            r = DotMap({'type': self.ARRAY, 'items': self.__init_property(p['items'])})

            if 'faker' in p:
                r.faker = p.faker

            return r
        else:
            return p

    def __init_properties(self, node):
        result = DotMap()

        for k, v in node.properties.items():
            result[k] = self.__init_property(v)

        node.properties = result

        return node

    def init(self):
        return self.__init_property(self.schema)

    def __fake_property(self, p):
        """
        if '$ref' in p:
            if 'faker' in p:
                return fake_value(p.faker, self)
            else:
                p = self.__get_node(p['$ref'])
        """
        if p.type != self.OBJECT and p.type != self.ARRAY:
            return fake_value(p, self) if 'faker' in p else None
        elif p.type == self.OBJECT:
            return fake_value(p, self) if 'faker' in p else self.__fake_properties(p.properties)
        elif p.type == self.ARRAY and 'items' in p:
            n = fake_value(p, self) if 'faker' in p else 1
            return [self.__fake_property(p['items']) for _ in range(n)]

    def __fake_properties(self, properties):
        result = {}

        for k, v in properties.items():
            result[k] = self.__fake_property(v)

        return result

    def fake(self):
        self.schema = self.init()
        return self.__fake_property(self.schema)

    def fake_node(self, node):
        return self.__fake_properties(node.properties) if 'properties' in node else self.__fake_property(node)

    def add_seed(self, seed):
        self.seeds[seed.name] = seed
        seed.set_df(self)

    def get_seed(self, name):
        return self.seeds[name]

    @staticmethod
    def save(data, name, dst='db', options=None):
        if dst == 'db':
            options = DotMap(options)
            if options.host is not 'localhost':
                client = MongoClient(host=options.host, port=options.port, username=options.user, password=options.password)
            else:
                client = MongoClient(host=options.host, port=options.port)

            db = client[options.db]
            collection = db[name]
            #collection.remove()
            res = collection.insert_many(data)
            return res
        elif dst == 'file':
            with open(name, 'w') as f:
                f.write(json.dumps(data, indent=2))
                return True
        else:
            return None
