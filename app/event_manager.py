"""
Только Менеджер может создавать и обновлять события
"""
from dataclasses import dataclass
from datetime import datetime

from app.models import DatetimeInterval, Event, EventType
from app.protocols import Repository


class ManagerConfig:pass


class BaseEventManager:

    def __init__(self, repo: Repository) -> None:
        self._repo = repo


@dataclass
class CreateRequest:
    type_name: str
    start: datetime
    end: datetime

    title: str | None = None
    describe: str | None = None


class Creator(BaseEventManager):
    def create_event(self, request: CreateRequest) -> Event:
        interval = DatetimeInterval(request.start, request.end)

        event_type = self._repo.event_type.get(request.type_name)

        event = Event(
                type=event_type, 
                datetime_interval=interval, 
                title=request.title,
                describe=request.describe,
            )
        self._repo.event.save(event)
        return event

    def create_type(self, name: str, color: str) -> None:
        type_ = EventType(name, color)
        self._repo.event_type.create(type_)


@dataclass
class EventUpdate:
    """
    Что должен содержать? 
    Только title и describe. 
    Если происходит замена типа и/или интервала,
    то будет происходить последовательно удаление, 
    а после создание новго Event
    """

    title: str | None = None
    describe: str | None = None


@dataclass
class EventTypeUpdate:
    name: str | None
    color: str | None


class Updater(BaseEventManager):

    def update_event(self, event: Event, update: EventUpdate) -> Event:
        if event.title == update.title and event.describe == update.describe:
            return event
        
        event.title = update.title
        event.describe = update.describe

        return self._repo.event.update(event)


    def update_type(self, type_: EventType, update: EventTypeUpdate) -> None:
        if type_.name == update.name and type_.color == update.color:
            return
        
        type_.name = update.name
        type_.color = update.color

        self._repo.event_type.update(type_)


class Deleter(BaseEventManager):

    def delete_event(self, event: Event) -> bool:
        return self._repo.event.delete(event)

    def delete_type(self, type_: EventType) -> bool:
        return self._repo.event_type.delete()


class Getter(BaseEventManager):
    def get_event(self, type_: EventType, date_interval: DatetimeInterval) -> list[Event]:
        return self._repo.event.get(type_, date_interval)

    def get_type(self, name: str) -> EventType:
        return self._repo.event_type.get_by_name(name)


class EventManager(Creator, Updater, Deleter, Getter):
    pass
