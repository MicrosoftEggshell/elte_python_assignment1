import json
from .models import Organizer, Joiner, Event


class EventFileManager:
    FILE_PATH = 'event.json'

    @classmethod
    def read_events_from_file(cls):
        try:
            with open(cls.FILE_PATH) as f:
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
