import json
from typing import List
from .models import Organizer, Joiner, Event


class EventFileManager:
    FILE_PATH = 'event.json'

    @classmethod
    def read_events_from_file(cls):
        try:
            with open(cls.FILE_PATH, encoding='utf-8') as f:
                content = json.load(f)
            events = []
            for event in content:
                event['organizer'] = Organizer(**event['organizer'])
                try:
                    event['joiners'] = [Joiner(**j) for j in event['joiners']]
                except KeyError:
                    pass
                events.append(Event(**event))
            return events
        except (OSError, json.JSONDecodeError):
            return []
    
    @classmethod
    def write_events_to_file(cls, events: List[Event]):
        with open(cls.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(
                events,
                f,
                ensure_ascii=False,
                indent=4,
                default=lambda x: x.__dict__
                )
