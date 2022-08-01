from .read_parameters import read_parameters
from ._retrieve_helpers import _get_simulation_info, _extract_parameters, _parameters_map
from .xml_to_dict import xml_to_dict
from .connection import Connection
import os
import tqdm

def retrieve(experiment_folder:str):
    _ChasteOutputRetriever().retrieve_experiment(experiment_folder)

def store_analysis(experiment_id:int, data:dict):
    _ChasteOutputRetriever().load_analysis(experiment_id, data)
            

class _ChasteOutputRetriever:
    def __init__(self, db_file='gastric_gland.db'):
        self.conn = Connection(db_file)

    def retrieve_simulation(self, simulation_folder:str):
        assert os.path.exists(simulation_folder), \
            f'Could not find simulation folder "{simulation_folder}"'
        experiment_name, simulation_id = _get_simulation_info(simulation_folder)
        output_folder = os.path.join(simulation_folder, 'results_from_time_0')
        version_id = self.load_version(
            os.path.join(output_folder, 'build.info'))
        experiment_id = self.load_experiment(
            version_id, experiment_name, simulation_id, output_folder)
        self.load_parameters(experiment_id,
            os.path.join(output_folder, 'results.parameters'))

    def retrieve_experiment(self, experiment_folder:str):
        assert os.path.exists(experiment_folder), \
            f'Could not find experiment folder "{experiment_folder}"'
        sims = os.listdir(experiment_folder)
        for simulation in tqdm.tqdm(sims):
            if not simulation.startswith('sim_'): continue
            self.retrieve_simulation(os.path.join(experiment_folder, simulation))

    def load_version(self, info_file:str):
        assert os.path.exists(info_file), f'Cannot find build info file "{info_file}"'
        build_info = xml_to_dict(open(info_file, 'r').read())
        return self.conn.get_version_id(
            build_info['ChasteBuildInfo']['ProvenanceInfo']['VersionString'],
            build_info['ChasteBuildInfo']['ProvenanceInfo']['Projects']['Project']['Name'],
            build_info['ChasteBuildInfo']['ProvenanceInfo']['Projects']['Project']['Version'],
            build_info['ChasteBuildInfo']['ProvenanceInfo']['BuildTime'])

    def load_experiment(self, version_id:int, experiment_name:str, simulation_id:int, output_folder:str):
        return self.conn.create_experiment(
            version_id, experiment_name, simulation_id, output_folder)

    def load_parameters(self, experiment_id:int, parameters_file:str):
        assert os.path.exists(parameters_file), f'Cannot find parameters file "{parameters_file}"'
        parameters = xml_to_dict(open(parameters_file, 'r').read())
        parameters = _extract_parameters(parameters)
        for k, value in parameters.items():
            if k in _parameters_map:
                self.conn.load_parameter(experiment_id, _parameters_map[k], value)

    def load_analysis(self, experiment_id:int, data:dict):
        for name,results in data.items():
            if type(results)!=dict:
                results=results.result
            for t,result in results.items():
                self.conn.load_analysis_result(experiment_id, name, result, t)
