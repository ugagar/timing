from dataclasses import dataclass
from datetime import datetime


@dataclass
class DatetimeInterval:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:

        if self.end.timestamp - self.start.timestamp == 0:
            raise ValueError("Неверно задан интервал: интервал не должен быть точкой")
        
        elif self.end.timestamp - self.start.timestamp < 0:
            raise ValueError("Неверно задан интервал: конечное значени должно быть больше начального")


@dataclass
class EventType:
    """
    Тип события. 
    В приложении будет достаточно выбрать тип и можно задавать интервалы событий
    Например, добавть типы: работа, учеба, спорт, отдых.
        Выбирать типы и отмечать их в календаре. Если потребуется можно указать Заголовок и описание события
    """
    name: str
    color: str # Не уверен что правильно смешивать тут представление пользовательское и работу алгоритма

    def __post_init__(self) -> None:
        # Добавить проверку цвета
        ...


@dataclass
class Event:
    type: EventType
    datetime_interval: DatetimeInterval

    title: str | None = None
    describe: str| None = None