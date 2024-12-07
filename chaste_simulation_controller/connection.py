import sqlite3
import threading
import multiprocessing
import pathlib
import collections.abc
import logging
import time
import typing
import pathlib
import itertools


class Connection:
    def get_connection(self):
        id = (multiprocessing.current_process().ident, threading.current_thread().ident)
        if id not in self.connections:
            self.connections[id] = sqlite3.connect(self.database, check_same_thread=False, timeout=300, *self.args, **self.kwargs)
            logging.debug(f'Opened database connection tid: {id}')
        return self.connections[id]
    
    def execute(self, *args, **kwargs):
        try:
            self.get_connection().execute(*args, **kwargs)
        except Exception as e:
            raise e
        
    def executescript(self, *args, **kwargs):
        try:
            self.get_connection().executescript(*args, **kwargs)
        except Exception as e:
            raise e

    def repeat_execute(self, *args, **kwargs):
        while True:
            try:
                self.execute(*args, **kwargs)
            except Exception as e:
                print(f"{e}, waiting 10s")
                self.close_connection()
                time.sleep(10)


    def close_connection(self):
        id = (multiprocessing.current_process().ident, threading.current_thread().ident)
        if id in self.connections:
            self.connections[id].close()
            del self.connections[id]
            logging.debug(f'Closed database connection tid: {id}')

    
    def commit(self):
        id = (multiprocessing.current_process().ident, threading.current_thread().ident)
        if id in self.connections:
            self.connections[id].commit()

    def __del__(self):
        n = len(self.connections)
        for c in self.connections.values():
            c.close()
        logging.info(f'Closed {n} database connections.')

    def __init__(self, database:str='controller.db', *args, **kwargs):
        self.database = database
        self.args = args
        self.kwargs = kwargs
        self.connections = {}
        if not pathlib.Path(self.database).exists():
            logging.info("Creating controller database")
            self.executescript(pathlib.Path(__file__).parent.joinpath('_sql', '_create_database.sql').open('r').read())
            self.commit()
            self.close_connection()
    
    def insert_job(self, experiment_name:str, simulation_id:int, args, sequence_id:int=-1, sequence_num:int=-1, prev_point_id:int=-1):
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO jobs(experiment_name, simulation_id, args)
                VALUES (?,?,?) ON CONFLICT DO UPDATE SET
                        args = excluded.args;
            """, (experiment_name, simulation_id, args))
            job_id = cur.lastrowid
            # cur.execute("""
            #     INSERT INTO sequence_points(sequence_id, job_id, sequence_num, previous_id)
            #     VALUES (?,?,?,?);
            # """, (sequence_id, job_id, sequence_num, prev_point_id))
            cur.close()
            self.commit()
        except Exception as e:
            raise e
        finally:
            self.close_connection()

    def insert_jobs(self, experiment_name:str, args_list, simulation_ids=None):
        try:
            conn:sqlite3.Connection = self.get_connection()
            if simulation_ids is None: simulation_ids = list(range(len(args_list)))
            conn.executemany("INSERT INTO jobs(experiment_name, simulation_id, args) VALUES (:name,:id,:args) ON CONFLICT DO UPDATE SET args=excluded.args;",
                             [dict(name=experiment_name, id=id, args=args) for id, args in zip(simulation_ids, args_list)])
            self.commit()
        except Exception as e:
            raise e
        finally:
            self.close_connection()

    def try_request_job(self, handler_id)->dict:
        try:
            timeout = 0
            
            conn = self.get_connection()
            cur = conn.cursor()

            cur.execute("SELECT id, experiment_name, simulation_id, args FROM jobs WHERE started_at IS NULL ORDER BY RANDOM() LIMIT 1;")
            r = cur.fetchone()
            if r is None:
                timeout = 10
                return None
            cur.execute("UPDATE jobs SET started_at=CURRENT_TIMESTAMP, handler_id=? \
                WHERE id=? AND started_at IS NULL AND handler_id IS NULL;", (handler_id, r[0]))
            cur.execute("SELECT handler_id FROM jobs WHERE id=?", (r[0],))
            r2 = cur.fetchone()
            if r2[0] != handler_id:
                timeout = 1
                raise RuntimeError(f"Collision on handler {handler_id} against {r2[0]}")
            cur.close()
            self.commit()
            
            s = f"--ID={r[1]} "+\
                f"--IT={int(r[2]):06d} {r[3].strip()}"
            job_info = dict(
                job_id=f"{r[0]}",
                experiment_name=f"{r[1]}",
                simulation_id=f"{int(r[2]):06d}",
                args=f"{s}"
            )
            return job_info
        except Exception as e:
            raise e
        finally:
            cur.close()
            self.close_connection()
            if timeout > 0:
                time.sleep(timeout)

    def notify_finished_job(self, job_id)->bool:
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE jobs SET completed_at=CURRENT_TIMESTAMP WHERE id=?", (job_id,))
            cur.close()
            self.commit()
        except Exception as e:
            raise e
        finally:
            self.close_connection()

