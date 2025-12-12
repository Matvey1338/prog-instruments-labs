import sqlite3
from datetime import datetime, date
from typing import List, Dict
from loguru import logger

from app.config import DB_PATH
from app.data.models import TimeEntry

class DatabaseHandler:
    def __init__(self):
        self._init_db()

    def _init_db(self) -> None:
        query_timer = """
        CREATE TABLE IF NOT EXISTS time_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT
        )
        """
        query_activity = """
        CREATE TABLE IF NOT EXISTS activities (
            date TEXT NOT NULL,
            app_name TEXT NOT NULL,
            seconds INTEGER DEFAULT 0,
            PRIMARY KEY (date, app_name)
        )
        """
        try:
            with self._get_connection() as conn:
                conn.execute(query_timer)
                conn.execute(query_activity)
            logger.debug("Проверка/создание таблиц БД выполнена")
        except sqlite3.Error as e:
            logger.critical(f"Ошибка инициализации БД: {e}")  # <--- CRITICAL
            raise

    def add_entry(self, entry: TimeEntry) -> None:
        if not entry.end_time:
            return

        query = "INSERT INTO time_entries (task_name, start_time, end_time) VALUES (?, ?, ?)"
        try:
            with self._get_connection() as conn:
                conn.execute(query, (
                    entry.task_name,
                    entry.start_time.isoformat(),
                    entry.end_time.isoformat()
                ))
            logger.debug(f"Запись сохранена в БД: {entry.task_name}")  # <--- DEBUG
        except sqlite3.Error as e:
            logger.error(f"Ошибка сохранения записи: {e}") # <--- ERROR

    def get_all_entries(self) -> List[TimeEntry]:
        query = "SELECT id, task_name, start_time, end_time FROM time_entries ORDER BY id DESC"
        entries = []
        with self._get_connection() as conn:
            for row in conn.execute(query):
                entries.append(TimeEntry(
                    id=row[0], task_name=row[1],
                    start_time=datetime.fromisoformat(row[2]),
                    end_time=datetime.fromisoformat(row[3]) if row[3] else None
                ))
        return entries

    def update_task_name(self, eid: int, name: str):
        with self._get_connection() as conn:
            conn.execute("UPDATE time_entries SET task_name = ? WHERE id = ?", (name, eid))

    def delete_entry(self, eid: int):
        with self._get_connection() as conn:
            conn.execute("DELETE FROM time_entries WHERE id = ?", (eid,))

    def increment_app_usage(self, app_name: str, seconds: int = 1) -> None:
        today_str = date.today().isoformat()
        query = """
        INSERT INTO activities (date, app_name, seconds) VALUES (?, ?, ?)
        ON CONFLICT(date, app_name) DO UPDATE SET seconds = seconds + ?
        """
        try:
            with self._get_connection() as conn:
                conn.execute(query, (today_str, app_name, seconds, seconds))
        except sqlite3.OperationalError:
            pass

    def get_today_stats(self) -> Dict[str, int]:
        today_str = date.today().isoformat()
        query = "SELECT app_name, seconds FROM activities WHERE date = ? ORDER BY seconds DESC"
        data = {}
        with self._get_connection() as conn:
            for row in conn.execute(query, (today_str,)):
                data[row[0]] = row[1]
        return data