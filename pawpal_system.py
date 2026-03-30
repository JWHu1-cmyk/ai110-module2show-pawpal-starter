from dataclasses import dataclass, field


@dataclass
class CareTask:
    title: str
    category: str
    duration_minutes: int
    priority: int  # higher = more important
    completed: bool = False

    def edit(self, title: str = None, duration_minutes: int = None, priority: int = None) -> None:
        """Update task fields in place."""
        if title is not None:
            self.title = title
        if duration_minutes is not None:
            self.duration_minutes = duration_minutes
        if priority is not None:
            self.priority = priority

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def compare_priority(self, other: "CareTask") -> int:
        """Return positive if self has higher priority, negative if lower, 0 if equal."""
        return self.priority - other.priority


@dataclass
class Pet:
    name: str
    species: str
    notes: str = ""
    tasks: list[CareTask] = field(default_factory=list)

    def add_care_task(self, task: CareTask) -> None:
        """Append a CareTask to this pet's task list."""
        self.tasks.append(task)

    def list_tasks(self) -> list[CareTask]:
        """Return all care tasks for this pet."""
        return list(self.tasks)


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def update_profile(self, name: str = None, available_minutes: int = None, preferences: dict = None) -> None:
        """Update owner profile fields."""
        if name is not None:
            self.name = name
        if available_minutes is not None:
            self.available_minutes_per_day = available_minutes
        if preferences is not None:
            self.preferences = preferences

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[CareTask]:
        """Gather and return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.list_tasks())
        return all_tasks


class Planner:
    def __init__(self) -> None:
        self.explanation: str = ""

    def build_daily_plan(self, owner: Owner, pet: Pet, tasks: list[CareTask] = None) -> list[CareTask]:
        """Select and order tasks into a daily plan that fits the owner's time budget.

        Sorts tasks by priority (highest first), then greedily adds tasks
        until the owner's available minutes are exhausted.
        """
        if tasks is None:
            tasks = pet.list_tasks()

        budget = owner.available_minutes_per_day
        sorted_tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)

        plan = []
        total_minutes = 0
        skipped = []

        for task in sorted_tasks:
            if total_minutes + task.duration_minutes <= budget:
                plan.append(task)
                total_minutes += task.duration_minutes
            else:
                skipped.append(task)

        self.explanation = self._build_explanation(plan, skipped, total_minutes, budget)
        return plan

    def explain_plan(self, plan: list[CareTask]) -> str:
        """Return the stored explanation from the most recent build_daily_plan call."""
        return self.explanation

    def _fits_within_budget(self, tasks: list[CareTask], minutes: int) -> bool:
        """Check whether total duration of tasks fits within the given minutes."""
        return sum(t.duration_minutes for t in tasks) <= minutes

    def _build_explanation(self, plan: list[CareTask], skipped: list[CareTask],
                           used_minutes: int, budget: int) -> str:
        """Generate a human-readable explanation of the plan."""
        lines = []
        lines.append(f"Daily plan uses {used_minutes} of {budget} available minutes.")

        if plan:
            lines.append("Scheduled tasks (highest priority first):")
            for i, task in enumerate(plan, 1):
                lines.append(f"  {i}. {task.title} ({task.category}) — "
                             f"{task.duration_minutes} min, priority {task.priority}")

        if skipped:
            lines.append("Skipped (not enough time):")
            for task in skipped:
                lines.append(f"  - {task.title} ({task.category}) — "
                             f"{task.duration_minutes} min, priority {task.priority}")

        return "\n".join(lines)
