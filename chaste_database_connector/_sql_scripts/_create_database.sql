
CREATE TABLE IF NOT EXISTS versions
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_string TEXT,
    project_name TEXT,
    project_version TEXT,
    build_time TIMESTAMP
);
CREATE UNIQUE INDEX IF NOT EXISTS version_index
    ON versions(version_string, project_name, project_version);


CREATE TABLE IF NOT EXISTS experiments
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_id INTEGER,
    experiment_name TEXT REQUIRED,
    simulation_id INTEGER REQUIRED,
    output_folder TEXT REQUIRED,
    startpoint_experiment_id INTEGER,

    FOREIGN KEY (version_id) REFERENCES versions(id),
    FOREIGN KEY (startpoint_experiment_id) REFERENCES experiments(id)
);
CREATE INDEX IF NOT EXISTS experiments_version_index
    ON experiments(version_id);
CREATE UNIQUE INDEX IF NOT EXISTS experiments_index
    ON experiments(version_id, experiment_name, simulation_id);

CREATE TABLE IF NOT EXISTS value_types
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value_type TEXT REQUIRED
);
CREATE UNIQUE INDEX IF NOT EXISTS value_type_index
    ON value_types(value_type);
INSERT INTO
    value_types(id, value_type)
VALUES
    (1, "int"),
    (2, "float"),
    (3, "string"),
    (4, "bool"),
    (5, "null")
ON CONFLICT (value_type) DO NOTHING;


CREATE TABLE IF NOT EXISTS parameter_types
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parameter_name TEXT REQUIRED,
    value_type_id INTEGER,

    FOREIGN KEY (value_type_id) REFERENCES value_types(id)
);
CREATE UNIQUE INDEX IF NOT EXISTS parameter_name_index
    ON parameter_types(parameter_name);


CREATE TABLE IF NOT EXISTS parameters
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id INTEGER REQUIRED,
    parameter_type_id INTEGER REQUIRED,
    parameter_value TEXT REQUIRED,
    notes TEXT,

    FOREIGN KEY (experiment_id) REFERENCES experiments(id),
    FOREIGN KEY (parameter_type_id) REFERENCES parameter_types(id)
);
CREATE INDEX IF NOT EXISTS parameters_experiment_index
    ON parameters(experiment_id);
CREATE INDEX IF NOT EXISTS parameters_parameter_type_index
    ON parameters(parameter_type_id);
CREATE UNIQUE INDEX IF NOT EXISTS parameters_index
    ON parameters(experiment_id, parameter_type_id);


CREATE TABLE IF NOT EXISTS analysis_types
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_name TEXT,
    value_type_id INTEGER,

    FOREIGN KEY (value_type_id) REFERENCES value_type(id)
);
CREATE UNIQUE INDEX IF NOT EXISTS analysis_types_index
    ON analysis_types(analysis_name);

CREATE TABLE IF NOT EXISTS analysis_results
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id INTEGER REQUIRED,
    analysis_type_id INTEGER REQUIRED,
    analysis_timepoint float,
    analysis_result TEXT REQUIRED,
    document JSON,
    
    FOREIGN KEY (experiment_id) REFERENCES experiments(id),
    FOREIGN KEY (analysis_type_id) REFERENCES analysis_types(id)
);
CREATE INDEX IF NOT EXISTS analysis_experiment_index
    ON analysis_results(experiment_id);
CREATE INDEX IF NOT EXISTS analysis_analysis_type_index
    ON analysis_results(analysis_type_id);
CREATE INDEX IF NOT EXISTS experiment_analysis_type_index
    ON analysis_results(experiment_id, analysis_type_id);
CREATE UNIQUE INDEX IF NOT EXISTS analysis_result_index
    ON analysis_results(experiment_id, analysis_type_id, analysis_timepoint);
