import time
import threading
import ctypes
import psutil
from typing import Optional
from loguru import logger
from app.data.database import DatabaseHandler


class AppMonitor:
    def __init__(self, db_handler: DatabaseHandler):
        self.db = db_handler
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self._interval = 5

    def start(self):
        if self.running:
            return
        logger.info("Запуск монитора активных окон")  # <--- INFO
        self.running = True
        self.thread = threading.Thread(target = self._loop, daemon = True)
        self.thread.start()

    def stop(self):
        logger.info("Остановка монитора активных окон")
        self.running = False
        if self.thread:
            self.thread.join()

    def _loop(self):
        while self.running:
            try:
                app_name = self._get_active_window_process_name()

                if app_name:
                    # Используем trace или debug, чтобы не засорять основной лог,
                    logger.debug(f"Активное окно: {app_name}")  # <--- DEBUG
                    self.db.increment_app_usage(app_name, self._interval)

            except Exception as e:
                # Логируем ошибку, но не роняем приложение
                logger.error(f"Ошибка в цикле мониторинга: {e}")  # <--- ERROR

            time.sleep(self._interval)

    def _get_active_window_process_name(self) -> Optional[str]:
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            if hwnd == 0:
                return None

            pid = ctypes.c_ulong()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

            process = psutil.Process(pid.value)
            return process.name()
        except Exception as e:
            # Например, access denied
            logger.warning(f"Не удалось получить имя процесса: {e}")  # <--- WARNING
            return None