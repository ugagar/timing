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


class EventCreator(BaseEventManager):
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

    def create_event_type(self, name: str, color: str):
        type_ = EventType(name, color)
        self._repo.event_type.create(type_)

