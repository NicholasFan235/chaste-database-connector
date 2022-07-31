
import pandas as pd

def read_parameters(params_filename:str):
    return _ParametersReader().read_file(params_filename)

class _ParametersReader:
    def __init__(self):
        pass

    def read_file(self, params_filename:str):
        params = pd.read_xml(params_filename, elems_only=True)\
            .melt().drop_duplicates().dropna(axis=0, how='any', subset=['value'])
        assert not params.duplicated('variable').any()
        return params.set_index('variable').to_dict()['value']
