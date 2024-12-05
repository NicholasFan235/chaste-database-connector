import pathlib
import pandas as pd
import numpy as np
import sqlite3
import chaste_simulation_controller as csc
import json
from itertools import product
import pprint
import pandas as pd

np.set_printoptions(precision=2)

experiment_name = 'test-parameter-sweep'

default_parameters = json.load(open(pathlib.Path(__file__).parent.joinpath('default_parameters.json')))

## Additional parameter options
parameter_variations = dict(
    FrictionStrength=np.linspace(1,5,10, dtype=float),
    TumourHypoxicConcentration=np.linspace(0.05,0.6,12, dtype=float)
)

seed_variations = dict(
    Seed=[0],
    ConfigurationSeed=[0],
)
print("Parameter variations:")
pprint.pprint(parameter_variations)
print("\nSeed variations:")
pprint.pprint(seed_variations)

parameter_sets = csc.all_parameter_combinations(parameter_variations)
seed_sets = csc.all_parameter_combinations(seed_variations)

arguments_list = list(map(csc.args_from_params_dict, [default_parameters.copy() | parameter_set | seed_set for parameter_set, seed_set in product(parameter_sets, seed_sets)]))


## Insert parameters
db = csc.Connection(pathlib.Path(__file__).parent.joinpath('controller.db'))
db.insert_jobs(experiment_name, arguments_list)

print()
print(pd.read_sql("SELECT COUNT(*) as n_jobs FROM jobs;", db.get_connection()))
db.close_connection()

