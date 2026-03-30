from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CareTask:
    title: str
    category: str
    duration_minutes: int
    priority: int  # higher = more important

    def edit(self, title: str = None, duration_minutes: int = None, priority: int = None) -> None:
        """Update task fields in place."""
        pass

    def compare_priority(self, other: "CareTask") -> int:
        """Return positive if self has higher priority, negative if lower, 0 if equal."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    notes: str = ""
    tasks: list[CareTask] = field(default_factory=list)

    def add_care_task(self, task: CareTask) -> None:
        """Append a CareTask to this pet's task list."""
        pass

    def list_tasks(self) -> list[CareTask]:
        """Return all care tasks for this pet."""
        pass


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int
    preferences: dict = field(default_factory=dict)

    def update_profile(self, name: str = None, available_minutes: int = None, preferences: dict = None) -> None:
        """Update owner profile fields."""
        pass


class Planner:
    def __init__(self) -> None:
        self.explanation: str = ""

    def build_daily_plan(self, owner: Owner, pet: Pet, tasks: list[CareTask]) -> list[CareTask]:
        """Select and order tasks into a daily plan that fits the owner's time budget."""
        pass

    def explain_plan(self, plan: list[CareTask]) -> str:
        """Return a human-readable explanation of why the plan was built this way."""
        pass

    def _fits_within_budget(self, tasks: list[CareTask], minutes: int) -> bool:
        """Check whether total duration of tasks fits within the given minutes."""
        pass
