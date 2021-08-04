from typing import List


def noop_formatters():
    return [lambda x: x]


def texto_para_numerico_duas_casas_decimais_formatters(tamanho):
    return [lambda x: x[:(tamanho - 2)] + '.' + x[(tamanho - 2):], lambda x: float(x.strip(' "'))]


def minuscula_formatters():
    return [lambda x: str(x).lower()]


def numerico_para_texto_duas_casas_decimais_formatters(tamanho, casas_decimais):
    return [lambda x: ("{:." + str(casas_decimais) + "f}").format(x).replace(".", ""), lambda x: str(x).zfill(tamanho)]


class Definition(object):
    def __init__(self, size: int, default_value, custom_formatters=None):
        if custom_formatters is None:
            custom_formatters = [lambda x: x]
        self.size = size
        self.default_value = default_value
        self.custom_formatters = custom_formatters


class Attribute(object):
    def __init__(self, name: str, definition: Definition):
        self.name = name
        self.definition = definition


class Schema(object):
    def __init__(self, name: str, attributes: List[Attribute], occurrences: int = 1):
        self.name = name
        self.attributes = attributes
        self.occurrences = occurrences


class StringToDict(object):
    def __init__(self, schema: Schema):
        self.schema = schema

    def parse_string(self, string_to_parse, dict_result=None, cursor=None) -> dict:
        if cursor is None:
            cursor = [0]
        if dict_result is None:
            dict_result = {}
        for attribute in self.schema.attributes:
            if isinstance(attribute, Attribute):
                result_value = string_to_parse[cursor[0]:(cursor[0] + attribute.definition.size)]
                for custom_formatter in attribute.definition.custom_formatters:
                    result_value = custom_formatter(result_value)
                dict_result[attribute.name] = result_value
                cursor[0] += attribute.definition.size
            if isinstance(attribute, Schema):
                if attribute.occurrences == 1:
                    attribute_nested = StringToDict(attribute).parse_string(string_to_parse, {}, cursor)
                    dict_result[attribute.name] = attribute_nested
                    return dict_result
                for i in range(attribute.occurrences):
                    attribute_nested = StringToDict(attribute).parse_string(string_to_parse, {}, cursor)
                    d = dict_result.setdefault(attribute.name, [])
                    if attribute.name not in d:
                        d.append(attribute_nested)
        return dict_result

    def parse_dict(self, dictionary, string_final=None, parent_path=""):
        if string_final is None:
            string_final = [""]
        for attribute in self.schema.attributes:
            path = attribute.name
            if parent_path != "":
                path = parent_path + "." + attribute.name
            if isinstance(attribute, Attribute):
                value = find_attribute_value_by_path(path, dictionary, attribute)
                string_final[0] += str(value)
            if isinstance(attribute, Schema):
                if attribute.occurrences == 1:
                    StringToDict(attribute).parse_dict(dictionary, string_final, path)
                    return
                for i in range(attribute.occurrences):
                    StringToDict(attribute).parse_dict(dictionary, string_final,
                                                       path + "." + str(i))
        return string_final[0]


def find_attribute_value_by_path(path_attribute, json, attribute: Attribute):
    keys = path_attribute.split('.')
    result_value = json
    for key in keys:
        try:
            string_int = int(key)
            result_value = result_value[string_int]
        except Exception:
            try:
                result_value = result_value[key]
            except Exception:
                result_value = str(attribute.definition.default_value) * attribute.definition.size
    for custom_formatter in attribute.definition.custom_formatters:
        result_value = custom_formatter(result_value)
    return result_value
