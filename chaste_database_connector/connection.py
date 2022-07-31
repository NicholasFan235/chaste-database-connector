
import sqlite3


class Connection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)

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
            output_folder:str, startpoint_experiment_id=None):
        self.query("""
            INSERT INTO experiments
                (version_id, experiment_name, simulation_id, output_folder, startpoint_experiment_id)
            VALUES
                (?,?,?,?,?)
            ON CONFLICT (version_id, experiment_name, simulation_id) DO NOTHING;""",
            (version_id, experiment_name, simulation_id, output_folder, startpoint_experiment_id))
        result = self.query_fetchone("SELECT id FROM experiments WHERE\
            experiments.version_id=? AND\
            experiments.experiment_name=? AND\
            experiments.simulation_id=?", (version_id, experiment_name, simulation_id))
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

    def load_parameter(self, experiment_id:int, parameter_name:str, parameter_value:str, notes:str=None):
        self.query("""
            INSERT INTO parameters
                (experiment_id, parameter_type_id, parameter_value, notes)
            VALUES
                (?,?,?,?)
            ON CONFLICT (experiment_id, parameter_type_id) DO NOTHING;""",
            (experiment_id, self.get_parameter_type_id(parameter_name), parameter_value, notes))

    def get_experiment_id(self, experiment_name:str, simulation_id:int, version_id:int=None):
        if version_id is None:
            result = self.query_fetchall("SELECT id FROM experiments WHERE\
                experiments.experiment_name=? AND\
                experiments.simulation_id=?", (experiment_name, simulation_id))
        else:
            result = self.query_fetchone("SELECT id FROM experiments WHERE\
                experiments.version_id=? AND\
                experiments.experiment_name=? AND\
                experiments.simulation_id=?", (version_id, experiment_name, simulation_id))
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

    def query(self, query:str, params=None):
        try:
            cur = self.conn.cursor()
            cur.execute(query, params)
        except Exception as e:
            raise e
        finally:
            cur.close()

    def query_fetchone(self, query:str, params=None):
        result = None
        try:
            cur = self.conn.cursor()
            cur.execute(query, params)
            result = cur.fetchone()
        except Exception as e:
            raise e
        finally:
            cur.close()
        return result
    
    def query_fetchall(self, query:str, params=None):
        result = None
        try:
            cur = self.conn.cursor()
            cur.execute(query, params)
            result = cur.fetchall()
        except Exception as e:
            raise e
        finally:
            cur.close()
        return result


    def __del__(self):
        self.conn.commit()
        self.conn.close()
