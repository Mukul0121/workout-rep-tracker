import sqlite3
import json
from datetime import datetime

DB_PATH = 'data/workouts.db'

def get_connection(path=None):
    conn = sqlite3.connect(path or DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(path=None):
    with get_connection(path) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise TEXT NOT NULL,
            reps INTEGER NOT NULL CHECK (reps >= 0),
            duration_sec INTEGER NOT NULL CHECK (duration_sec >= 0),
            tut_sec REAL DEFAULT 0.0,
            rep_tempos TEXT DEFAULT '[]',
            created_at TEXT NOT NULL)''')

def add_session(exercise, reps, duration_sec, tut_sec=0.0, rep_tempos='[]', path=None):
    init_db(path)
    with get_connection(path) as conn:
        cur = conn.execute(
            'INSERT INTO sessions (exercise, reps, duration_sec, tut_sec, rep_tempos, created_at) VALUES (?, ?, ?, ?, ?, ?)',
            (exercise, reps, duration_sec, tut_sec, rep_tempos, datetime.now().isoformat(timespec='seconds')))
        return cur.lastrowid

def list_sessions(exercise=None, path=None):
    init_db(path)
    sql, params = 'SELECT * FROM sessions', ()
    if exercise:
        sql, params = sql + ' WHERE exercise = ?', (exercise,)
    with get_connection(path) as conn:
        rows = conn.execute(sql + ' ORDER BY created_at DESC', params).fetchall()
    return [dict(r) for r in rows]

def get_stats(path=None):
    init_db(path)
    with get_connection(path) as conn:
        totals = conn.execute(
            'SELECT COUNT(*) AS sessions, COALESCE(SUM(reps), 0) AS total_reps FROM sessions').fetchone()
        best = conn.execute('SELECT exercise, MAX(reps) AS best_reps FROM sessions GROUP BY exercise').fetchall()
        daily = conn.execute(
            'SELECT DATE(created_at) AS day, SUM(reps) AS reps FROM sessions GROUP BY day ORDER BY day').fetchall()
    return {'sessions': totals['sessions'], 'total_reps': totals['total_reps'],
            'best': [dict(r) for r in best], 'daily': [dict(r) for r in daily]}