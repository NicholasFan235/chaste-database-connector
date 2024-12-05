CREATE TABLE sequences(
    id INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE jobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    args TEXT REQUIRED,
    experiment_name TEXT REQUIRED,
    simulation_id INTEGER REQUIRED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    processed_at TIMESTAMP,
    handler_id TEXT
);
CREATE UNIQUE INDEX jobs_index ON jobs(experiment_name, simulation_id); 

CREATE TABLE sequence_points(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence_id INTEGER,
    sequence_num INTEGER,
    job_id INTEGER,
    previous_id INTEGER,
    accepted BOOLEAN,
    evaluation REAL,
    end_time REAL DEFAULT 0,

    FOREIGN KEY (sequence_id) REFERENCES sequences(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (previous_id) REFERENCES smc_sequence(id)
);
CREATE INDEX sequence_points_index ON sequence_points(sequence_id, previous_id, accepted);
CREATE UNIQUE INDEX sequence_point_job_index ON sequence_points(job_id);
