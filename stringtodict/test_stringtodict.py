from unittest import TestCase

from stringtodict import Attribute, Definition, Schema, StringToDict, texto_para_numerico_formatters, \
    minuscula_formatters, numerico_para_texto_formatters


def gerar_schema_serializador_desserializador():
    attribute_name = Attribute("name", Definition(size=6, default_value=" "))
    attribute_address = Attribute("address", Definition(size=2, default_value=" "))
    attribute_local = Attribute("local", Definition(size=1, default_value=" "))
    attribute_value = Attribute("value", Definition(size=1, default_value=" "))
    attribute_flag = Attribute("flag", Definition(size=1, default_value=" "))

    schema_sub_nested = Schema(name="nested_sub", attributes=[attribute_flag])
    schema_nested = Schema(name="nested", attributes=[attribute_local, attribute_value, schema_sub_nested],
                           occurrences=2)
    schema = Schema(attributes=[attribute_name, attribute_address, schema_nested, attribute_flag])

    return schema


def gerar_schema_desserializador():
    attribute_name = Attribute(name="name",
                               definition=Definition(size=4, custom_formatters=texto_para_numerico_formatters(4, 2)))
    attribute_address = Attribute(name="address",
                                  definition=Definition(size=4, custom_formatters=texto_para_numerico_formatters(4, 2)))
    attribute_local = Attribute(name="local",
                                definition=Definition(size=6,
                                                      custom_formatters=minuscula_formatters()))
    attribute_value = Attribute(name="value",
                                definition=Definition(size=5, custom_formatters=texto_para_numerico_formatters(5, 2)))
    attribute_flag = Attribute(name="flag", definition=Definition(size=1))

    schema_sub_nested = Schema(name="nested_sub", attributes=[attribute_flag])
    schema_nested = Schema(name="nested", attributes=[attribute_local, attribute_value, schema_sub_nested],
                           occurrences=2)
    schema_desserializador = Schema(attributes=[attribute_name, attribute_address, schema_nested, attribute_flag])

    return schema_desserializador


def gerar_schema_serializador():
    attribute_name = Attribute(name="name",
                               definition=Definition(size=4, custom_formatters=numerico_para_texto_formatters(4, 2)))
    attribute_address = Attribute(name="address",
                                  definition=Definition(size=4, custom_formatters=numerico_para_texto_formatters(4, 2)))
    attribute_local = Attribute(name="local",
                                definition=Definition(size=6, default_value=" ",
                                                      custom_formatters=minuscula_formatters()))
    attribute_value = Attribute(name="value",
                                definition=Definition(size=5, custom_formatters=numerico_para_texto_formatters(5, 2)))
    attribute_flag = Attribute(name="flag", definition=Definition(size=1, default_value=" "))

    schema_sub_nested = Schema(name="nested_sub", attributes=[attribute_flag])
    schema_nested = Schema(name="nested", attributes=[attribute_local, attribute_value, schema_sub_nested],
                           occurrences=2)
    schema_serializador = Schema(attributes=[attribute_name, attribute_address, schema_nested, attribute_flag])

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

    def test_numerico_para_texto_formatters(self):
        result_value = 678.9
        for custom_formatter in numerico_para_texto_formatters(5, 2):
            result_value = custom_formatter(result_value)
        self.assertEqual("67890", result_value)

        result_value = 6.789

        for custom_formatter in numerico_para_texto_formatters(5, 3):
            result_value = custom_formatter(result_value)

        self.assertEqual("06789", result_value)

    def test_texto_para_numerico_formatters(self):
        result_value = "67890"
        for custom_formatter in texto_para_numerico_formatters(5, 2):
            result_value = custom_formatter(result_value)
        self.assertEqual(678.9, result_value)

        result_value = "06789"

        for custom_formatter in texto_para_numerico_formatters(5, 3):
            result_value = custom_formatter(result_value)

        self.assertEqual(6.789, result_value)

    def test_deve_dessserializar_string_em_dicionario_com_sucesso(self):
        schema_desserializador = gerar_schema_desserializador()
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

        result_dict = StringToDict(schema_desserializador).parse_string(text)

        self.assertEqual(dictionary, result_dict)

    def test_deve_dessserializar_string_com_valor_name_zerado_em_dicionario_com_sucesso(self):
        schema_desserializador = gerar_schema_desserializador()
        text = "000045678901234567890123456789012"
        dictionary = {
            'name': 0.0,
            'address': 45.67,
            'nested': [
                {'local': '890123', 'value': 456.78, 'nested_sub': {'flag': '9'}},
                {'local': '012345', 'value': 678.9, 'nested_sub': {'flag': '1'}}
            ],
            'flag': '2',
        }

        result_dict = StringToDict(schema_desserializador).parse_string(text)

        self.assertEqual(dictionary, result_dict)

    def test_deve_serializar_dicionario_em_string_com_sucesso(self):
        schema_serializador = gerar_schema_serializador()
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

        result_text = StringToDict(schema_serializador).parse_dict(dictionary)

        self.assertEqual(text, result_text)

    def test_deve_serializar_dicionario_em_string_com_sucesso_dicionario_vazio(self):
        schema_serializador = gerar_schema_serializador()
        text = "00000000      00000       00000  "
        dictionary = {}

        result_text = StringToDict(schema_serializador).parse_dict(dictionary)

        self.assertEqual(text, result_text)

    def test_deve_serializar_dicionario_com_name_zerado_em_string_com_sucesso(self):
        schema_serializador = gerar_schema_serializador()
        text = "000045678901234567890123456789012"
        dictionary = {
            'name': 0.0,
            'address': 45.67,
            'nested': [
                {'local': '890123', 'value': 456.78, 'nested_sub': {'flag': '9'}},
                {'local': '012345', 'value': 678.9, 'nested_sub': {'flag': '1'}}
            ],
            'flag': '2',
        }

        result_text = StringToDict(schema_serializador).parse_dict(dictionary)

        self.assertEqual(text, result_text)

    def test_deve_serializar_dicionario_com_name_nao_informado_em_string_com_sucesso(self):
        schema_serializador = gerar_schema_serializador()
        text = "000045678901234567890123456789012"
        dictionary = {
            'address': 45.67,
            'nested': [
                {'local': '890123', 'value': 456.78, 'nested_sub': {'flag': '9'}},
                {'local': '012345', 'value': 678.9, 'nested_sub': {'flag': '1'}}
            ],
            'flag': '2',
        }

        result_text = StringToDict(schema_serializador).parse_dict(dictionary)

        self.assertEqual(text, result_text)

    def test_deve_converter_texto_em_dicionario_com_campo_numerico(self):
        attribute_name = Attribute("name", Definition(size=4, custom_formatters=texto_para_numerico_formatters(4, 2)))
        schema = Schema(attributes=[attribute_name])
        text_a = "0534"
        text_b = "0000"
        dictionary_a = {
            'name': 5.34
        }
        dictionary_b = {
            'name': 0.0
        }

        result_dict_a = StringToDict(schema).parse_string(text_a)
        result_dict_b = StringToDict(schema).parse_string(text_b)

        self.assertEqual(dictionary_a, result_dict_a)
        self.assertEqual(dictionary_b, result_dict_b)

    def test_deve_converter_texto_com_todos_os_campos_em_dicionario_1(self):
        result = StringToDict(self.schema).parse_string(self.text)
        self.assertEqual(result, self.dictionary)

    def test_deve_converter_dicionario_com_todos_os_campos_em_texto_mantendo_o_tamanho_final_1(self):
        result_string = StringToDict(self.schema).parse_dict(self.dictionary)
        self.assertEqual(result_string, self.text)

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

        self.assertEqual(dictionary, result)

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

        self.assertEqual(result_string, text)

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

        self.assertEqual(result_string, text)

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

        self.assertEqual(result_string, text)

    def test_deve_converter_dicionario_sem_todos_os_campos_em_texto_mantendo_o_tamanho_final_5(self):
        text = "        IJK   O"
        dictionary = {
            'nested': [
                {'local': 'I', 'value': 'J', 'nested_sub': {'flag': 'K'}}
            ],
            'flag': 'O',
        }

        result_string = StringToDict(self.schema).parse_dict(dictionary)

        self.assertEqual(result_string, text)

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

        self.assertEqual(result_string, text)

    def test_deve_converter_dicionario_em_texto_em_minuscula(self):
        attribute_name = Attribute("name",
                                   Definition(size=6, default_value=" ", custom_formatters=minuscula_formatters()))
        schema = Schema(attributes=[attribute_name])
        text_a = "abcdef"
        text_b = "      "
        dictionary_a = {
            'name': 'ABCDEF'
        }
        dictionary_b = {}
        result_string_a = StringToDict(schema).parse_dict(dictionary_a)
        result_string_b = StringToDict(schema).parse_dict(dictionary_b)

        self.assertEqual(result_string_a, text_a)
        self.assertEqual(result_string_b, text_b)

    def test_deve_converter_dicionario_com_numero_em_texto(self):
        definition = Definition(size=2)
        attribute_name = Attribute(name="name", definition=definition)
        schema = Schema(attributes=[attribute_name])
        text_a = "55"
        dictionary_a = {
            'name': 55
        }
        text_b = "00"
        dictionary_b = {}

        result_string_a = StringToDict(schema).parse_dict(dictionary_a)
        result_string_b = StringToDict(schema).parse_dict(dictionary_b)

        self.assertEqual(1, len(definition.custom_formatters))
        self.assertEqual(result_string_a, text_a)
        self.assertEqual(result_string_b, text_b)

    def test_deve_converter_dicionario_com_numero_em_texto_sem_ponto(self):
        attribute_name = Attribute(name="name",
                                   definition=Definition(size=4,
                                                         custom_formatters=numerico_para_texto_formatters(
                                                             4, 2)))
        schema = Schema(attributes=[attribute_name])
        text_a = "0534"
        dictionary_a = {
            'name': 5.34
        }
        text_b = "0000"
        dictionary_b = {}

        result_string_a = StringToDict(schema).parse_dict(dictionary_a)
        result_string_b = StringToDict(schema).parse_dict(dictionary_b)

        self.assertEqual(text_a, result_string_a)
        self.assertEqual(text_b, result_string_b)

    def test_deve_lancar_excecao_dicionario_vazio(self):
        schema = Schema()
        dictionary_a = None
        with self.assertRaises(ValueError) as context:
            StringToDict(schema).parse_dict(dictionary_a)
        self.assertTrue('Empty dictionary not allowed' in str(context.exception))
