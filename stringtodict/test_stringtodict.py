from unittest import TestCase

from stringtodict import Attribute, Definition, Schema, StringToDict


def generateSchema():
    attribute_name = Attribute("name", Definition(6, " "))
    attribute_address = Attribute("address", Definition(2, " "))
    attribute_local = Attribute("local", Definition(1, " "))
    attribute_value = Attribute("value", Definition(1, " "))
    attribute_flag = Attribute("flag", Definition(1, " "))

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

    def test_parse_string_complete_0(self):
        result = StringToDict(self.schema).parse_string(self.text)
        self.assertEqual(result, self.dictionary, 'Não foi possível converter texto em dicionário')

    def test_parse_dict_complete_0(self):
        result_string = StringToDict(self.schema).parse_dict(self.dictionary)
        self.assertEqual(result_string, self.text, 'Não foi possível converter dicionário em texto')

    def test_parse_string_incomplete_0(self):
        text = "ABCDEFGHIJK   O"
        dictionary = {
            'name': 'ABCDEF',
            'address': 'GH',
            'nested': [
                {'local': 'I', 'value': 'J', 'nested_sub': {'flag': 'K'}},
                {'local': ' ', 'value': ' ', 'nested_sub': {'flag': ' '}}
            ],
            'flag': 'O',
        }
        result = StringToDict(self.schema).parse_string(text)
        self.assertEqual(dictionary, result, 'Não foi possível converter texto em dicionário')

    def test_parse_dict_with_incomplete_nested_0(self):
        text = "ABCDEFGHIJK   O"
        dictionary = {
            'name': 'ABCDEF',
            'address': 'GH',
            'nested': [
                {'local': 'I', 'value': 'J', 'nested_sub': {'flag': 'K'}}
            ],
            'flag': 'O',
        }
        result_string = StringToDict(self.schema).parse_dict(dictionary)
        self.assertEqual(result_string, text, 'Não foi possível converter dicionário em texto')

    def test_parse_dict_with_incomplete_sub_nested_0(self):
        text = "ABCDEFGHIJ    O"
        dictionary = {
            'name': 'ABCDEF',
            'address': 'GH',
            'nested': [
                {'local': 'I', 'value': 'J'}
            ],
            'flag': 'O',
        }
        result_string = StringToDict(self.schema).parse_dict(dictionary)
        self.assertEqual(result_string, text, 'Não foi possível converter dicionário em texto')

    def test_parse_dict_with_incomplete_0(self):
        text = "ABCDEF  IJK   O"
        dictionary = {
            'name': 'ABCDEF',
            'nested': [
                {'local': 'I', 'value': 'J', 'nested_sub': {'flag': 'K'}}
            ],
            'flag': 'O',
        }
        result_string = StringToDict(self.schema).parse_dict(dictionary)
        self.assertEqual(result_string, text, 'Não foi possível converter dicionário em texto')

    def test_parse_dict_with_incomplete_1(self):
        text = "        IJK   O"
        dictionary = {
            'nested': [
                {'local': 'I', 'value': 'J', 'nested_sub': {'flag': 'K'}}
            ],
            'flag': 'O',
        }
        result_string = StringToDict(self.schema).parse_dict(dictionary)
        self.assertEqual(result_string, text, 'Não foi possível converter dicionário em texto')

    def test_parse_dict_with_incomplete_2(self):
        text = "ABCDEF  I K   O"
        dictionary = {
            'name': 'ABCDEF',
            'nested': [
                {'local': 'I', 'nested_sub': {'flag': 'K'}}
            ],
            'flag': 'O',
        }
        result_string = StringToDict(self.schema).parse_dict(dictionary)
        self.assertEqual(result_string, text, 'Não foi possível converter dicionário em texto')

    def test_parse_dict_with_custom_formatter_0(self):
        attribute_name = Attribute("name", Definition(6, " ", [lambda x: str(x).lower()]))
        schema = Schema("root", [attribute_name])
        text = "abcdef"
        dictionary = {
            'name': 'ABCDEF'
        }
        result_string = StringToDict(schema).parse_dict(dictionary)
        self.assertEqual(result_string, text, 'Não foi possível converter dicionário em texto')

    def test_parse_dict_with_custom_formatter_1(self):
        attribute_name = Attribute("name", Definition(2, "00", [lambda x: x]))
        schema = Schema("root", [attribute_name])
        text = "55"
        dictionary = {
            'name': 55
        }
        result_string = StringToDict(schema).parse_dict(dictionary)
        self.assertEqual(result_string, text, 'Não foi possível converter dicionário em texto')

    def test_parse_string_with_custom_formatter_2(self):
        attribute_name = Attribute("name",
                                   Definition(4, "0", [lambda x: str(x).replace(".", ""), lambda x: str(x).zfill(4)]))
        schema = Schema("root", [attribute_name])
        text = "0534"
        dictionary = {
            'name': 5.34
        }
        result_string = StringToDict(schema).parse_dict(dictionary)
        self.assertEqual(text, result_string, 'Não foi possível converter dicionário em texto')
