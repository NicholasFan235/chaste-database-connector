
INSERT INTO
    analysis_types(analysis_name, value_type_id)
VALUES
    ("foveolar_height", 2),
    ("foveolar_min_height", 2),
    ("foveolar_max_height", 2),
    ("neck_height", 2),
    ("neck_min_height", 2),
    ("neck_max_height", 2),
    ("downward_migration", 2),
    ("min_cell_size", 2),
    ("max_cell_count", 2),
    ("max_neck_cells", 2),
    ("max_foveolar_cells", 2),
    ("average_base_lifespan", 2),
    ("average_isthmus_lifespan", 2),
    ("average_foveolar_lifespan", 2),
    ("average_neck_lifespan", 2),
    ("max_gland_height", 2),
    ("min_gland_height", 2),
    ("average_death_rate", 2),
    ("average_birth_rate", 2),
    ("average_isthmus_birth_rate", 2),
    ("average_base_birth_rate", 2),
    ("average_isthmus_cycle_time", 2),
    ("average_base_cycle_time", 2)
ON CONFLICT (analysis_name) DO NOTHING;