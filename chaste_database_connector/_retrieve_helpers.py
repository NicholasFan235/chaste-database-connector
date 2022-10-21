from pathlib import Path
import re

def _get_simulation_info(simulation_folder:str):
    simulation_path = Path(simulation_folder)
    experiment_name = _get_experiment_info(simulation_path.parent)
    simulation_name = simulation_path.name
    match  = re.match('sim_(?P<simulation_id>\d+)', simulation_name)
    assert match is not None, f'Invalid simulation name: "{simulation_name}"'
    return experiment_name, int(match.group('simulation_id'))

def _get_experiment_info(experiment_folder):
    experiment_path = Path(experiment_folder)
    experiment_name = experiment_path.name
    return experiment_name


def _extract_parameters(parameters:dict):
    params = {}
    for k,v in parameters.items():
        if v is None:
            continue
        elif type(v) == dict:
            params.update(_extract_parameters(v))
        elif type(v) == str:
            params[k] = v
        elif type(v) == list:
            raise NotImplementedError('Not Implemented interpretation of listparameters')
        else:
            raise Exception(f'Unexpected type found in parameters dict: {type(v)}')
    return params


_parameters_map = {
    'CryptCircumference': 'crypt_circumference',
    'UseFixedBottomCells': 'use_fixed_bottom_cells',
    'MaxCells': 'max_cells',
    'Dt': 'dt',
    'EndTime': 'end_time',
    'UpdateCellPopulation': 'update_cell_population',
    'SamplingTimestepMultiple': 'sampling_timestep_multiple',
    'UpdatingTimestepMultiple': 'updating_timestep_multiple',
    'OutputDivisionLocations': 'output_division_locations',
    'OutputCellVelocities': 'output_cell_velocities',
    'MechanicsCutOffLength': 'mechanics_cutoff_length',
    'UseVariableRadii': 'use_variable_radii',
    'MitosisRequiredSize': 'mitosis_required_size',
    'FoveolarSizeMultiplier': 'foveolar_size_multiplier',
    'GhostSpringStiffness': 'ghost_spring_stiffness',
    'UseAreaBasedDampingConstant': 'use_area_based_damping_constant',
    'AreaBasedDampingConstantParameter': 'area_based_damping_constant_parameter',
    'MeinekeDivisionSeparation': 'meineke_division_separation',
    'DampingConstantNormal': 'damping_constant',
    'DampingConstantMutant': 'damping_constant_mutant',
    'IsthmusBeginHeight': 'isthmus_begin_height',
    'IsthmusEndHeight': 'isthmus_end_height',
    'BaseHeight': 'base_height',
    'BaseG1Duration': 'base_g1_duration',
    'IsthmusG1Duration': 'isthmus_g1_duration',
    'StemCellG1Duration': 'stem_g1_duration',
    'TransitCellG1Duration': 'transit_g1_duration',
    'SDuration': 's_duration',
    'G2Duration': 'g2_duration',
    'MDuration': 'm_duration',
    'CutoffAge': 'cutoff_age',
    'UseEdgeBasedSpringConstant': 'use_edge_based_spring_constant',
    'UseBCatSprings': 'use_beta_cat_springs',
    'UseApoptoticSprings': 'use_apoptotic_springs',
    'BetaCatSpringScaler': 'beta_cat_spring_scaler',
    'ApoptoticSpringTensionStiffness': 'apoptotic_spring_tension_stiffness',
    'ApoptoticSpringCompressionStiffness': 'apoptotic_spring_compression_stiffness',
    'MeinekeSpringStiffness': 'meineke_spring_stiffness',
    'MeinekeDivisionRestingSpringLength': 'meineke_division_resting_spring_length',
    'MeinekeSpringGrowthDuration': 'meineke_spring_growth_duration',
    'UseCutOffLength': 'use_cutoff_length',
    'CutOffLength': 'cutoff_length',
    'UseAdaptiveTimestep': 'use_adaptive_timestep',
    'UseUpdateNodeLocation': 'use_update_node_location',
    'GhostNodeForcesEnabled': 'ghost_node_forces_enabled',
    'MinCellCycleDuration': 'min_cell_cycle_duration',
    'MaxCellCycleDuration': 'max_cell_cycle_duration',
    'HypoxicConcentration': 'hypoxic_concentration',
    'NecroticConcentration': 'necrotic_concentration',
    'QuiescenceVolumeProportion': 'quiescence_volume_proportion'
}