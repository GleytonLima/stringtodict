from unittest import TestCase

from stringtodict import Attribute, Definition, Schema, StringToDict


def generateSchema():
    attribute_name = Attribute("name", Definition(6))
    attribute_address = Attribute("address", Definition(2))
    attribute_local = Attribute("local", Definition(1))
    attribute_value = Attribute("value", Definition(1))
    attribute_flag = Attribute("flag", Definition(1))

    schema_sub_nested = Schema("nested_sub", [attribute_flag])
    schema_nested = Schema("nested", [attribute_local, attribute_value, schema_sub_nested], 2)
    schema = Schema("root", [attribute_name, attribute_address, schema_nested, attribute_flag])

    return schema


class TestStringToDict(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = generateSchema()
        cls.text = "ABCDEFGHIJKLMNO"
        cls.dictionary = {
            'name': 'ABCDEF',
            'address': 'GH',
            'nested': [
                {'local': 'I', 'value': 'J', 'nested_sub': {'flag': 'K'}},
                {'local': 'L', 'value': 'M', 'nested_sub': {'flag': 'N'}}
            ],
            'flag': 'O',
        }

    def test_parse_string(self):
        result = StringToDict(self.schema).parse_string(self.text)
        self.assertEqual(result, self.dictionary, 'Não foi possível converter texto em dicionário')

    def test_parse_dict(self):
        result_string = StringToDict(self.schema).parse_dict(self.dictionary)
        self.assertEqual(result_string, self.text, 'Não foi possível converter dicionário em texto')
