from datetime import datetime
from typing import Optional, Dict
from loguru import logger

from app.data.models import TimeEntry
from app.data.database import DatabaseHandler
from app.core.monitor import AppMonitor


class TimerController:
    def __init__(self):
        logger.debug("Инициализация контроллера")
        self.db = DatabaseHandler()
        self.monitor = AppMonitor(self.db)

        # Данные таймера
        self.current_start_time: Optional[datetime] = None
        self.current_task_name: str = ""
        self.is_running: bool = False

        # Запускаем фоновый мониторинг сразу при старте приложения
        self.monitor.start()

    def stop_all_threads(self):
        """Вызывать при полном выходе."""
        logger.info("Остановка всех фоновых потоков...")
        self.monitor.stop()

    def start_timer(self, task_name: str) -> None:
        if not task_name.strip():
            task_name = "Без названия"

        logger.info(f"Старт таймера: '{task_name}'")

        self.current_task_name = task_name
        self.current_start_time = datetime.now()
        self.is_running = True

    def stop_timer(self) -> Optional[TimeEntry]:
        if not self.is_running or not self.current_start_time:
            logger.warning("Попытка остановить таймер, который не был запущен.")
            return None

        end_time = datetime.now()
        entry = TimeEntry(
            task_name = self.current_task_name,
            start_time = self.current_start_time,
            end_time = end_time
        )

        self.db.add_entry(entry)

        # Расчет длительности для лога
        duration = (end_time - self.current_start_time).total_seconds()
        logger.info(
            f"Таймер остановлен. Задача: '{self.current_task_name}', Длительность: {duration:.2f} сек.")

        self.is_running = False
        self.current_start_time = None
        return entry

    def get_elapsed_time_str(self) -> str:
        if not self.is_running or not self.current_start_time: return "00:00:00"
        delta = datetime.now() - self.current_start_time
        total_seconds = int(delta.total_seconds())
        h, r = divmod(total_seconds, 3600)
        m, s = divmod(r, 60)
        return f"{h:02}:{m:02}:{s:02}"

    def get_history(self) -> list[TimeEntry]:
        return self.db.get_all_entries()

    def rename_task(self, entry_id: int, new_name: str) -> None:
        if new_name.strip(): self.db.update_task_name(entry_id, new_name)

    def delete_task(self, entry_id: int) -> None:
        self.db.delete_entry(entry_id)

    def get_activity_stats(self) -> Dict[str, int]:
        return self.db.get_today_stats()