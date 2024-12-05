
import sqlite3
import time
import os
import sys
import random
import chaste_simulation_controller as csc

def main():
    db = csc.Connection()
    job_id = sys.argv[1]

    while (os.path.exists('running.flag')):
        try:
            db.notify_finished_job(job_id)
            break
        except Exception as e:
            sys.stderr.write(str(e) + '\n')
        finally:
            db.close_connection()


if __name__ == "__main__":
    main()
