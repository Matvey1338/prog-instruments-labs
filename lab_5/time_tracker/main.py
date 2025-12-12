from loguru import logger
from app.ui.main_window import TimeTrackerApp
from app.core.logger import setup_logging

if __name__ == "__main__":
    setup_logging()

    logger.info("Инициализация приложения...")

    # Запускаем GUI
    try:
        app = TimeTrackerApp()
        app.mainloop()
    except Exception as e:
        logger.critical(f"Приложение упало с ошибкой: {e}")
    finally:
        logger.info("Завершение работы.")