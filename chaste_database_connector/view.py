from .connection import Connection
import pandas as pd

class View:
    def __init__(self, db_file='gastric_gland.db'):
        self.conn = Connection(db_file)

    def view_experiments(self):
        return pd.read_sql("""
            SELECT experiments.id, experiment_name, simulation_id, output_folder, version_string, project_name, project_version
            FROM experiments
                INNER JOIN versions ON versions.id=experiments.version_id
            ORDER BY version_id,experiment_name,simulation_id;""",
            self.conn.conn).set_index('id')

    def view_experiment_parameters(self, experiment_name:str, simulation_id:int, version_id:int=None):
        experiment_id = self.conn.get_experiment_id(experiment_name, simulation_id, version_id)
        return self.conn.get_parameters_for_experiment(experiment_id)


    def view_all_parameters(self, experiment_name:str):
        df = pd.read_sql("""
            SELECT experiment_name, simulation_id, parameter_name, parameter_value FROM parameters
                INNER JOIN experiments ON experiments.id = parameters.experiment_id
                INNER JOIN parameter_types ON parameter_types.id = parameters.parameter_type_id
            WHERE
                experiment_name=?
            ORDER BY simulation_id;
        """, self.conn.conn, params=(experiment_name,))
        return df.pivot(['experiment_name', 'simulation_id'], 'parameter_name', 'parameter_value')

    def view_all_analysis_results(self, experiment_name:str):
        df = pd.read_sql("""
            SELECT experiment_name, simulation_id, analysis_name, analysis_timepoint, analysis_result
            FROM analysis_results
                INNER JOIN experiments ON experiments.id = analysis_results.experiment_id
                INNER JOIN analysis_types ON analysis_types.id = analysis_results.analysis_type_id
            WHERE
                experiment_name=?
            ORDER BY simulation_id;
        """, self.conn.conn, params=(experiment_name,))
        return df.pivot(['experiment_name', 'simulation_id', 'analysis_timepoint'], 'analysis_name', 'analysis_result')
