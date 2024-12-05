
import sqlite3
import time
import os
import sys
import random
import chaste_simulation_controller as csc


def main():
    db = csc.Connection()
    handler_id = sys.argv[1]
    
    while os.path.exists('running.flag'):
        try:
            job_info = db.try_request_job(handler_id)
            if job_info is None: continue

            sys.stdout.write(f"{job_info['job_id']}\n")
            sys.stdout.write(f"{job_info['experiment_name']}\n")
            sys.stdout.write(f"{job_info['simulation_id']}\n")
            sys.stdout.write(f"{job_info['args']}\n")
            sys.stderr.write(f"Started simulation, {job_info['experiment_name']} {job_info['simulation_id']}\n")
            break
        except Exception as e:
            sys.stderr.write(str(e) + '\n')


if __name__ == "__main__":
    main()
