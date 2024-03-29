from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event
from .file_storage import EventFileManager

router = APIRouter()


@router.get("/events", response_model=List[Event])
async def get_all_events():
    return EventFileManager.read_events_from_file()


@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):
    events = EventFileManager.read_events_from_file()
    return [event for event in events if(
        date       in (None, event.date)           and
        organizer  in (None, event.organizer.name) and
        status     in (None, event.status)         and
        event_type in (None, event.type)
    )]


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    events = EventFileManager.read_events_from_file()
    for event in events:
        if event.id == event_id:
            return event
    raise HTTPException(404, 'Event not found')


@router.post("/events", response_model=Event)
async def create_event(event: Event):
    events = EventFileManager.read_events_from_file()
    if any(e.id == event.id for e in events):
        raise HTTPException(409, 'Event ID already exists')
    events.append(event)
    EventFileManager.write_events_to_file(events)
    return event


@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    if event.id != event_id:
        raise HTTPException(409, 'Cannot modify event ID')
    events = EventFileManager.read_events_from_file()
    for e in events:
        if e.id == event_id:
            events.remove(e)
            events.append(event)
            EventFileManager.write_events_to_file(events)
            return event
    raise HTTPException(404, 'Event Not found')


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    events = EventFileManager.read_events_from_file()
    for e in events:
        if e.id == event_id:
            events.remove(e)
            EventFileManager.write_events_to_file(events)
            return 'Event deleted successfully'
    raise HTTPException(404, 'Event Not found')


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    pass
