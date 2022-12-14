
import sqlite3
import time
import sys
import random


class Connection:
    def __init__(self, db_file, *args, **kwargs):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file, *args, **kwargs)

    def get_version_id(self, version_string:str, project_name:str, project_version:str, build_time:str):
        self.query("""
            INSERT INTO versions
                (version_string, project_name, project_version, build_time)
            VALUES
                (?,?,?,?)
            ON CONFLICT (version_string, project_name, project_version) DO NOTHING;""",
            (version_string, project_name, project_version, build_time))
        result = self.query_fetchone("SELECT id FROM versions WHERE\
            versions.version_string=? AND\
            versions.project_name=? AND\
            versions.project_version=?", (version_string, project_name, project_version))
        assert result is not None
        return result[0]

    def create_experiment(self, version_id:int, experiment_name:str, simulation_id:int,
            output_folder:str, startpoint_experiment_id=None, results_from_time:int=0):
        self.query("""
            INSERT INTO experiments
                (version_id, experiment_name, simulation_id, output_folder,
                startpoint_experiment_id, results_from_time)
            VALUES
                (?,?,?,?,?,?)
            ON CONFLICT (version_id, experiment_name, simulation_id, results_from_time) DO NOTHING;""",
            (version_id, experiment_name, simulation_id, output_folder,
            startpoint_experiment_id, results_from_time))
        result = self.query_fetchone("SELECT id FROM experiments WHERE\
            experiments.version_id=? AND\
            experiments.experiment_name=? AND\
            experiments.simulation_id=? AND\
            experiments.results_from_time=?", (version_id, experiment_name, simulation_id, results_from_time))
        assert result is not None
        return result[0]

    def get_parameter_type_id(self, parameter_name:str):
        #self.query("""INSERT INTO parameter_types(parameter_name)
        #    VALUES (?)
        #    ON CONFLICT (parameter_name) DO NOTHING;""", (parameter_name,))
        result = self.query_fetchone("""
            SELECT id FROM parameter_types
            WHERE parameter_types.parameter_name=?;""", (parameter_name,))
        assert result is not None, f'Unable to get parameter_id for "{parameter_name}"'
        return result[0]

    def get_parameter_value(self, experiment_id:int, parameter_name:str):
        r = self.query_fetchone("""
            SELECT parameter_value FROM parameters WHERE
            experiment_id=? AND
            parameter_type_id=?;""",
            (experiment_id, self.get_parameter_type_id(parameter_name)))
        assert r is not None, f'Unable to find parameter {parameter_name} for experiment {experiment_id}'
        return r[0]

    def load_parameter(self, experiment_id:int, parameter_name:str, parameter_value:str, notes:str=None):
        self.query("""
            INSERT INTO parameters
                (experiment_id, parameter_type_id, parameter_value, notes)
            VALUES
                (?,?,?,?)
            ON CONFLICT (experiment_id, parameter_type_id) DO NOTHING;""",
            (experiment_id, self.get_parameter_type_id(parameter_name), parameter_value, notes))

    def get_experiment_id(self, experiment_name:str, simulation_id:int, version_id:int=None, results_from_time:int=0):
        if version_id is None:
            result = self.query_fetchall("SELECT id FROM experiments WHERE\
                experiments.experiment_name=? AND\
                experiments.simulation_id=? AND\
                experiments.results_from_time=?", (experiment_name, simulation_id, results_from_time))
        else:
            result = self.query_fetchall("SELECT id FROM experiments WHERE\
                experiments.version_id=? AND\
                experiments.experiment_name=? AND\
                experiments.simulation_id=? AND\
                experiments.results_from_time=?", (version_id, experiment_name, simulation_id, results_from_time))
        assert result is not None, f'Unable to find experiment {experiment_name}, simulation {simulation_id}'
        assert len(result) == 1, f'Multiple experiments found for {experiment_name} simulation {simulation_id}, try poviding version_id'
        return result[0][0]
    
    def get_parameters_for_experiment(self, experiment_id:int, include_notes=False):
        result = self.query_fetchall("""
            SELECT parameter_name, parameter_value, notes FROM parameters
                INNER JOIN parameter_types ON parameter_types.id = parameters.parameter_type_id
            WHERE experiment_id=?""", (experiment_id,))
        ret = {}
        for res in result:
            if include_notes:
                ret[res[0]] = (res[1],res[2])
            else:
                ret[res[0]] = res[1]
        return ret
    
    def get_or_create_analysis_id(self, analysis_name:str):
        self.query("""
            INSERT INTO analysis_types
                (analysis_name)
            VALUES
                (?)
            ON CONFLICT (analysis_name) DO NOTHING;""",
            (analysis_name,))
        result = self.query_fetchone("SELECT id FROM analysis_types WHERE\
            analysis_types.analysis_name=?", (analysis_name,))
        assert result is not None
        return result[0]

    def get_analysis_id(self, analysis_name:str):
        result = self.query_fetchone("SELECT id FROM analysis_types WHERE\
            analysis_types.analysis_name=?", (analysis_name,))
        assert result is not None
        return result[0]

    def load_analysis_result(self, experiment_id, analysis_type, analysis_result, timepoint):
        if type(analysis_type)==str:
            analysis_type = self.get_or_create_analysis_id(analysis_type)
        assert type(analysis_type)==int
        self.query("""
            INSERT INTO analysis_results
                (experiment_id, analysis_type_id, analysis_result, analysis_timepoint)
            VALUES
                (?,?,?,?)
            ON CONFLICT (experiment_id, analysis_type_id, analysis_timepoint)
            DO UPDATE SET analysis_result=excluded.analysis_result;
        """, (experiment_id, analysis_type, analysis_result, timepoint))

    def get_analysis_result(self, experiment_id, analysis_type, timepoint=None):
        if type(analysis_type)==str:
            analysis_type = self.get_analysis_id(analysis_type)
        assert type(analysis_type)==int
        if timepoint is None:
            result = self.query_fetchall("""
                SELECT analysis_timepoint, analysis_result FROM analysis_results
                WHERE experiment_id=? AND analysis_type_id=? ORDER BY analysis_timepoint DESC;
            """, (experiment_id, analysis_type))
            assert result is not None, "Unable to find analysis results"
            return result
        else:
            result = self.query_fetchone("""
                SELECT analysis_result FROM analysis_results
                WHERE experiment_id=? AND analysis_type=? AND analysis_timepoint=?;
            """, (experiment_id, analysis_type, timepoint))
            assert result is not None, "Unable to find analysis result"
            return result[0]


    def query(self, query:str, params=None, reps=10):
        for i in range(reps):
            try:
                cur = self.conn.cursor()
                cur.execute(query, params)
                return
            except Exception as e:
                if i >= 9: raise e
                sys.stderr.write(f"Encountered exception {e.str()}, retrying {i+1}/{reps}")
                time.sleep(random.randint(10,20))
            finally:
                cur.close()
            

    def query_fetchone(self, query:str, params=None, reps=10):
        result = None
        for i in range(reps):
            try:
                cur = self.conn.cursor()
                cur.execute(query, params)
                result = cur.fetchone()
                break
            except Exception as e:
                if i >= reps-1: raise e
                sys.stderr.write(f"Encountered exception {e.str()}, retrying {i+1}/{reps}")
                time.sleep(random.randint(10,20))
            finally:
                cur.close()
        return result
    
    def query_fetchall(self, query:str, params=None, reps=10):
        result = None
        for i in range(reps):
            try:
                cur = self.conn.cursor()
                cur.execute(query, params)
                result = cur.fetchall()
                break
            except Exception as e:
                if i >= reps-1: raise e
                sys.stderr.write(f"Encountered exception {e.str()}, retrying {i+1}/{reps}")
                time.sleep(random.randint(10, 20))
            finally:
                cur.close()
        return result


    def __del__(self):
        self.conn.commit()
        self.conn.close()
