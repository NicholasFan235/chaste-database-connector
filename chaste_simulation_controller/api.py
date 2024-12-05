import itertools


def all_parameter_combinations(variations:dict)->list[dict]:
    return [{k:v for k,v in zip(variations, parameter_set)} for parameter_set in itertools.product(*variations.values())]


def args_from_params_dict(params:dict)->str:
    return ' '.join([f'--{name.lstrip('--')}={value}' for name, value in params.items()])
