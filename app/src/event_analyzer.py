from typing import List
from .models import Event, Joiner


class EventAnalyzer:
    @classmethod
    def get_joiners_multiple_meetings_method(cls, events: List[Event]) -> List[Joiner]:
        single_joiners = []
        multi_joiners = []
        for event in events:
            if not event.joiners:
                continue
            for joiner in event.joiners:
                if joiner in multi_joiners:
                    continue
                if joiner in single_joiners:
                    multi_joiners.append(joiner)
                    single_joiners.remove(joiner)  # optional
                else:
                    single_joiners.append(joiner)
        return multi_joiners
