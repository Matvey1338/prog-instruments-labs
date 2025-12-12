from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TimeEntry:
    """Модель записи хронометража."""
    task_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    id: Optional[int] = None

    @property
    def duration(self) -> str:
        """Возвращает длительность в формате ЧЧ:ММ:СС."""
        if not self.end_time:
            return "В процессе..."

        delta = self.end_time - self.start_time
        total_seconds = int(delta.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    @property
    def date_str(self) -> str:
        """Возвращает дату старта в формате ДД.ММ.ГГГГ."""
        return self.start_time.strftime("%d.%m.%Y")