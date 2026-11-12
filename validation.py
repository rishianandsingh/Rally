from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class EventInput:
    title: str
    description: str
    team_size: int
    event_date: date

def validate_event(e: EventInput) -> list[str]:
    errors: list[str] = []
    if not e.title.strip():
        errors.append("Title is required.")
    if len(e.title) > 100:
        errors.append("Title must be 100 characters or fewer.")
    if not 2 <= e.team_size <= 10:
        errors.append("Team size must be between 2 and 10.")
    if e.event_date < date.today():
        errors.append("Event date cannot be in the past.")
    return errors