from typing import List


class Definition(object):
    def __init__(self, size: int):
        self.size = size


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
                dict_result[attribute.name] = string_to_parse[cursor[0]:(cursor[0] + attribute.definition.size)]
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
                value = find_attribute_value_by_path(path, dictionary)
                if isinstance(value, str):
                    string_final[0] += value
            if isinstance(attribute, Schema):
                if attribute.occurrences == 1:
                    StringToDict(attribute).parse_dict(dictionary, string_final, path)
                    return
                for i in range(attribute.occurrences):
                    StringToDict(attribute).parse_dict(dictionary, string_final,
                                                       path + "." + str(i))
        return string_final[0]


def find_attribute_value_by_path(path_attribute, json):
    keys = path_attribute.split('.')
    result_value = json
    for key in keys:
        try:
            string_int = int(key)
            result_value = result_value[string_int]
        except ValueError:
            try:
                result_value = result_value[key]
            except Exception:
                result_value = None
    return result_value