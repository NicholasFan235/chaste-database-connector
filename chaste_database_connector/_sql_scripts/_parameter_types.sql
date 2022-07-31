
INSERT INTO
    parameter_types(parameter_name, value_type_id)
VALUES
-- Simulation Parameters
    ("crypt_circumference", 1),
    ("use_fixed_bottom_cells", 4),
    ("max_cells", 1),
    ("dt", 2),
    ("end_time", 2),
    ("sampling_timestep_multiple", 1),
-- Population Parameters
    ("mitosis_required_size", 2),
    ("foveolar_size_multiplier", 2),
    ("ghost_spring_stiffness", 2),
    ("use_area_based_damping_constant", 4),
    ("area_based_damping_constant_parameter", 2),
    ("meineke_division_separation", 2),
    ("damping_constant", 2),
-- Cell Cycle Model Parameters
    ("base_height", 2),
    ("isthmus_begin_height", 2),
    ("isthmus_end_height", 2),
    ("base_g1_duration", 2),
    ("isthmus_g1_duration", 2),
    ("stem_g1_duration", 2),
    ("transit_g1_duration", 2),
    ("s_duration", 2),
    ("g2_duration", 2),
    ("m_duration", 2),
-- Cell Killer Parameters
    ("cutoff_age", 2),
-- Forces
    ("use_edge_based_spring_constant", 4),
    ("use_beta_cat_springs", 4),
    ("beta_cat_spring_scaler", 2),
    ("use_apoptotic_springs", 4),
    ("apoptotic_spring_tension_stiffness", 2),
    ("apoptotic_spring_compression_stiffness", 2),
    ("meineke_spring_stiffness", 2),
    ("meineke_division_resting_spring_length", 2),
    ("meineke_spring_growth_duration", 2),
    ("use_cutoff_length", 4),
    ("cutoff_length", 2),
-- Numerical Method
    ("use_adaptive_timestep", 4),
    ("use_update_node_location", 4),
    ("ghost_node_forces_enabled", 4)
ON CONFLICT (parameter_name) DO NOTHING;
