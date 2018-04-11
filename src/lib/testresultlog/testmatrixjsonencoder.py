import json

class TestEnvMatrixJsonEncoder(object):

    def start_encode(self, data_structure_obj):
        #encoder = json.JSONEncoder()
        #return encoder.encode(data_structure_obj)
        #return json.dumps(data_structure_obj, sort_keys=True, indent=4)
        #print('DEBUG: data_structure_obj : %s' % data_structure_obj)
        return json.dumps(data_structure_obj, sort_keys=True, indent=4)
