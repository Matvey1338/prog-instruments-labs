import sys
from pathlib import Path
from loguru import logger


def setup_logging():
    """Настройка конфигурации логгера."""

    # Определяем путь к логам (папка logs в корне проекта)
    # Используем pathlib для надежности путей на разных ОС
    log_path = Path("logs")
    log_path.mkdir(parents = True, exist_ok = True)  # Создаст папку, если её нет

    # Удаляем стандартный обработчик
    logger.remove()

    # 1. Логи в консоль
    logger.add(
        sys.stderr,
        level = "DEBUG",
        format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

    # 2. Логи в файл
    logger.add(
        log_path / "app.log",
        rotation = "1 MB",
        compression = "zip",
        level = "DEBUG",
        format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}",
        encoding = "utf-8"  # Важно для корректного отображения кириллицы в файле
    )

    logger.info("Система логгирования настроена успешно.")