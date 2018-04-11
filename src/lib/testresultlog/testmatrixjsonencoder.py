import json

class TestEnvMatrixJsonEncoder(object):

    def start_encode(self, data_structure_obj):
        return json.dumps(data_structure_obj, sort_keys=True, indent=4)
