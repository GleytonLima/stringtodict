from unittest import TestCase

from stringtodict import Attribute, Definition, Schema, StringToDict, texto_para_numerico_duas_casas_decimais_formatters, \
    minuscula_formatters, noop_formatters, numerico_para_texto_duas_casas_decimais_formatters


def gerar_schema_serializador_desserializador():
    attribute_name = Attribute("name", Definition(6, " "))
    attribute_address = Attribute("address", Definition(2, " "))
    attribute_local = Attribute("local", Definition(1, " "))
    attribute_value = Attribute("value", Definition(1, " "))
    attribute_flag = Attribute("flag", Definition(1, " "))

    schema_sub_nested = Schema("nested_sub", [attribute_flag])
    schema_nested = Schema("nested", [attribute_local, attribute_value, schema_sub_nested], 2)
    schema = Schema("root", [attribute_name, attribute_address, schema_nested, attribute_flag])

    return schema


def gerar_schema_desserializador():
    attribute_name = Attribute("name", Definition(4, "0", texto_para_numerico_duas_casas_decimais_formatters(4)))
    attribute_address = Attribute("address", Definition(4, "0", texto_para_numerico_duas_casas_decimais_formatters(4)))
    attribute_local = Attribute("local", Definition(6, " ", minuscula_formatters()))
    attribute_value = Attribute("value", Definition(5, "0", texto_para_numerico_duas_casas_decimais_formatters(5)))
    attribute_flag = Attribute("flag", Definition(1, " "))

    schema_sub_nested = Schema("nested_sub", [attribute_flag])
    schema_nested = Schema("nested", [attribute_local, attribute_value, schema_sub_nested], 2)
    schema_desserializador = Schema("root", [attribute_name, attribute_address, schema_nested, attribute_flag])

    return schema_desserializador


def gerar_schema_serializador():
    attribute_name = Attribute("name", Definition(4, "0", numerico_para_texto_duas_casas_decimais_formatters(4, 2)))
    attribute_address = Attribute("address", Definition(4, "0", numerico_para_texto_duas_casas_decimais_formatters(4, 2)))
    attribute_local = Attribute("local", Definition(6, " ", minuscula_formatters()))
    attribute_value = Attribute("value", Definition(5, "0", numerico_para_texto_duas_casas_decimais_formatters(5, 2)))
    attribute_flag = Attribute("flag", Definition(1, " "))

    schema_sub_nested = Schema("nested_sub", [attribute_flag])
    schema_nested = Schema("nested", [attribute_local, attribute_value, schema_sub_nested], 2)
    schema_serializador = Schema("root", [attribute_name, attribute_address, schema_nested, attribute_flag])

    return schema_serializador


class TestStringToDict(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = gerar_schema_serializador_desserializador()
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

    def test_numerico_para_texto_duas_casas_decimais_formatters(self):
        result_value = 678.9
        for custom_formatter in numerico_para_texto_duas_casas_decimais_formatters(5, 2):
            result_value = custom_formatter(result_value)
        self.assertEqual("67890", result_value, 'Não foi possível converter dicionário em texto')

    def test_deve_dessserializar_string_em_dicionario_com_sucesso(self):
        schema = gerar_schema_desserializador()
        text = "112345678901234567890123456789012"
        dictionary = {
            'name': 11.23,
            'address': 45.67,
            'nested': [
                {'local': '890123', 'value': 456.78, 'nested_sub': {'flag': '9'}},
                {'local': '012345', 'value': 678.9, 'nested_sub': {'flag': '1'}}
            ],
            'flag': '2',
        }
        result_dict = StringToDict(schema).parse_string(text)
        self.assertEqual(dictionary, result_dict, 'Não foi possível converter dicionário em texto')

    def test_deve_serializar_dicionario_em_string_com_sucesso(self):
        schema = gerar_schema_serializador()
        text = "112345678901234567890123456789012"
        dictionary = {
            'name': 11.23,
            'address': 45.67,
            'nested': [
                {'local': '890123', 'value': 456.78, 'nested_sub': {'flag': '9'}},
                {'local': '012345', 'value': 678.9, 'nested_sub': {'flag': '1'}}
            ],
            'flag': '2',
        }
        result_text = StringToDict(schema).parse_dict(dictionary)
        self.assertEqual(text, result_text, 'Não foi possível converter dicionário em texto')

    def test_deve_converter_texto_em_dicionario_com_campo_numerico(self):
        attribute_name = Attribute("name", Definition(4, "0", texto_para_numerico_duas_casas_decimais_formatters(4)))
        schema = Schema("root", [attribute_name])
        text = "0534"
        dictionary = {
            'name': 5.34
        }
        result_dict = StringToDict(schema).parse_string(text)
        self.assertEqual(dictionary, result_dict, 'Não foi possível converter dicionário em texto')

    def test_deve_converter_texto_com_todos_os_campos_em_dicionario_1(self):
        result = StringToDict(self.schema).parse_string(self.text)
        self.assertEqual(result, self.dictionary, 'Não foi possível converter texto em dicionário')

    def test_deve_converter_dicionario_com_todos_os_campos_em_texto_mantendo_o_tamanho_final_1(self):
        result_string = StringToDict(self.schema).parse_dict(self.dictionary)
        self.assertEqual(result_string, self.text, 'Não foi possível converter dicionário em texto')

    def test_deve_converter_dicionario_sem_todos_os_campos_em_texto_mantendo_o_tamanho_final_1(self):
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

    def test_deve_converter_dicionario_sem_todos_os_campos_em_texto_mantendo_o_tamanho_final_2(self):
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

    def test_deve_converter_dicionario_sem_todos_os_campos_em_texto_mantendo_o_tamanho_final_3(self):
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

    def test_deve_converter_dicionario_sem_todos_os_campos_em_texto_mantendo_o_tamanho_final_4(self):
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

    def test_deve_converter_dicionario_sem_todos_os_campos_em_texto_mantendo_o_tamanho_final_5(self):
        text = "        IJK   O"
        dictionary = {
            'nested': [
                {'local': 'I', 'value': 'J', 'nested_sub': {'flag': 'K'}}
            ],
            'flag': 'O',
        }
        result_string = StringToDict(self.schema).parse_dict(dictionary)
        self.assertEqual(result_string, text, 'Não foi possível converter dicionário em texto')

    def test_deve_converter_dicionario_sem_todos_os_campos_em_texto_mantendo_o_tamanho_final_6(self):
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

    def test_deve_converter_dicionario_em_texto_em_minuscula(self):
        attribute_name = Attribute("name", Definition(6, " ", minuscula_formatters()))
        schema = Schema("root", [attribute_name])
        text = "abcdef"
        dictionary = {
            'name': 'ABCDEF'
        }
        result_string = StringToDict(schema).parse_dict(dictionary)
        self.assertEqual(result_string, text, 'Não foi possível converter dicionário em texto')

    def test_deve_converter_dicionario_com_numero_em_texto(self):
        attribute_name = Attribute("name", Definition(2, "00", noop_formatters()))
        schema = Schema("root", [attribute_name])
        text = "55"
        dictionary = {
            'name': 55
        }
        result_string = StringToDict(schema).parse_dict(dictionary)
        self.assertEqual(result_string, text, 'Não foi possível converter dicionário em texto')

    def test_deve_converter_dicionario_com_numero_em_texto_sem_ponto(self):
        attribute_name = Attribute("name", Definition(4, "0", numerico_para_texto_duas_casas_decimais_formatters(4, 2)))
        schema = Schema("root", [attribute_name])
        text = "0534"
        dictionary = {
            'name': 5.34
        }
        result_string = StringToDict(schema).parse_dict(dictionary)
        self.assertEqual(text, result_string, 'Não foi possível converter dicionário em texto')
