import sqlite3
import os
from pathlib import Path

def create_database(db_file='gastric_gland.db', recreate=False):
    if os.path.exists(db_file):
        if recreate:
            print(f'Old database was deleted because recreate was set to True')
            os.remove(db_file)
        else:
            print(f'Database already exists ({db_file})')
            return
    
    with sqlite3.connect(db_file) as conn, \
        open(os.path.join(Path(__file__).parent,'_sql_scripts', '_create_database.sql'), 'r') as f:
        cur = conn.cursor()
        cur.executescript(f.read())
        cur.close()

def main():
    create_database()

if __name__ == '__main__':
    main()
