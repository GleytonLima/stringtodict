# Conversor de Texto em Dicionário de dados


1. Dado um `Schema`, um texto e o dicionário:

    ```python
        attribute_name = Attribute("name", Definition(6))
        attribute_address = Attribute("address", Definition(2))
        attribute_local = Attribute("local", Definition(1))
        attribute_value = Attribute("value", Definition(1))
        attribute_flag = Attribute("flag", Definition(1))
    
        schema_sub_nested = Schema("nested_sub", [attribute_flag])
        schema_nested = Schema("nested", [attribute_local, attribute_value, schema_sub_nested], 2)
        schema = Schema("root", [attribute_name, attribute_address, schema_nested, attribute_flag])
    ``` 
    
    ```python
    text = "ABCDEFGHIJKLMNO"
    ```
    
    ```python
    dictionary = {
                    'name': 'ABCDEF',
                    'address': 'GH',
                    'nested': [
                        {'local': 'I', 'value': 'J', 'nested_sub': {'flag': 'K'}},
                        {'local': 'L', 'value': 'M', 'nested_sub': {'flag': 'N'}}
                    ],
                    'flag': 'O',
                }
    ```
2. Para converter de texto em dicionário use:

    ```python
    result = StringToDict(schema).parse_string(text)
    ```
    O resultado será o dicionário.

3. Para converter um dicionário em texto use:
   
    ```python
    result = StringToDict(schema).parse_dict(dictionary)
    ```
    O resultado será o texto.