import json
class StringToDictConverter:
    @staticmethod
    def convert(str_data):
        dict_data = json.loads(str_data)
        return dict_data