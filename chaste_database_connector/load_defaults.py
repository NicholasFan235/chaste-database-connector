import sqlite3
import os
from pathlib import Path

def _run_script(cur, filename):
    with open(filename, 'r') as f:
        cur.executescript(f.read())

def load_defaults(db_file='gastric_gland.db'):
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        _run_script(cur, os.path.join(Path(__file__).parent,'_sql_scripts', '_parameter_types.sql'))
        _run_script(cur, os.path.join(Path(__file__).parent,'_sql_scripts', '_analysis_types.sql'))
        cur.close()

def main():
    create_database()

if __name__ == '__main__':
    main()
