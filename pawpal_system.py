from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from itertools import count
import json
from pathlib import Path


_task_ids = count(1)


def _set_next_task_id(next_id: int) -> None:
    global _task_ids
    _task_ids = count(next_id)


@dataclass
class Pet:
    """A pet whose care tasks can be scheduled."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task belonging to this pet."""
        if task.pet_name.casefold() != self.name.casefold():
            raise ValueError("task pet_name must match this pet")
        self.tasks.append(task)

    def list_tasks(self) -> list[Task]:
        """Return this pet's tasks in chronological order."""
        return sorted(self.tasks, key=lambda task: (task.due_date, task.time))


@dataclass
class Owner:
    """An owner and the pets they care for."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's household."""
        self.pets.append(pet)

    def add_task(self, task: Task) -> None:
        """Attach a task to the matching pet or reject an unknown pet."""
        pet = next((item for item in self.pets if item.name.casefold() == task.pet_name.casefold()), None)
        if pet is None:
            raise ValueError(f"No pet named {task.pet_name!r} belongs to this owner")
        pet.add_task(task)


@dataclass
class Task:
    """A care task scheduled for a pet."""

    title: str
    pet_name: str
    time: str
    duration_minutes: int = 20
    priority: str = "medium"
    due_date: date = field(default_factory=date.today)
    frequency: str = "none"
    completed: bool = False
    task_id: int = field(default_factory=lambda: next(_task_ids))

    def __post_init__(self) -> None:
        if len(self.time) != 5 or self.time[2] != ":":
            raise ValueError("time must use HH:MM format")
        hour, minute = self.time.split(":")
        if not (hour.isdigit() and minute.isdigit() and 0 <= int(hour) < 24 and 0 <= int(minute) < 60):
            raise ValueError("time must be a valid 24-hour HH:MM value")
        if self.duration_minutes < 1:
            raise ValueError("duration_minutes must be positive")
        if self.priority not in {"low", "medium", "high"}:
            raise ValueError("priority must be low, medium, or high")
        if self.frequency not in {"none", "daily", "weekly"}:
            raise ValueError("frequency must be none, daily, or weekly")

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


class Scheduler:
    """Store tasks and provide simple sorting, filtering, and recurrence logic."""

    def __init__(self, owner: Owner | None = None) -> None:
        self.owner = owner
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule."""
        self.tasks.append(task)
        if self.owner is not None:
            self.owner.add_task(task)

    def sort_by_time(self, tasks: list[Task] | None = None) -> list[Task]:
        """Return tasks in chronological HH:MM order without mutating input."""
        return sorted(tasks if tasks is not None else self.tasks, key=lambda task: task.time)

    def sort_by_priority(self, tasks: list[Task] | None = None) -> list[Task]:
        """Order high-priority tasks first, then by due date and time."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        selected = tasks if tasks is not None else self.tasks
        return sorted(selected, key=lambda task: (priority_order[task.priority], task.due_date, task.time))

    def next_available_slot(
        self,
        due_date: date,
        duration_minutes: int,
        start_time: str = "07:00",
        end_time: str = "22:00",
    ) -> str | None:
        """Find the earliest slot that fits without overlapping any task that date."""
        if duration_minutes < 1:
            raise ValueError("duration_minutes must be positive")
        slot_start = datetime.combine(due_date, time.fromisoformat(start_time))
        schedule_end = datetime.combine(due_date, time.fromisoformat(end_time))
        if slot_start >= schedule_end:
            return None

        busy_intervals = sorted(
            (
                datetime.combine(due_date, time.fromisoformat(task.time)),
                datetime.combine(due_date, time.fromisoformat(task.time))
                + timedelta(minutes=task.duration_minutes),
            )
            for task in self.tasks
            if task.due_date == due_date and not task.completed
        )
        candidate = slot_start
        requested_duration = timedelta(minutes=duration_minutes)
        for busy_start, busy_end in busy_intervals:
            if candidate + requested_duration <= busy_start:
                break
            if candidate < busy_end and candidate + requested_duration > busy_start:
                candidate = busy_end

        if candidate + requested_duration > schedule_end:
            return None
        return candidate.strftime("%H:%M")

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        """Filter tasks by pet name and/or completion state."""
        return [
            task
            for task in self.tasks
            if (pet_name is None or task.pet_name.casefold() == pet_name.casefold())
            and (completed is None or task.completed is completed)
        ]

    def detect_conflicts(self, tasks: list[Task] | None = None) -> list[str]:
        """Warn when tasks on the same date have identical start times."""
        scheduled = sorted(
            tasks if tasks is not None else self.tasks,
            key=lambda task: (task.due_date, task.time),
        )
        warnings = []
        for index, task in enumerate(scheduled):
            for other in scheduled[index + 1 :]:
                if (task.due_date, task.time) != (other.due_date, other.time):
                    break
                warnings.append(
                    f"{task.due_date.isoformat()} {task.time}: {task.title} ({task.pet_name}) conflicts with "
                    f"{other.title} ({other.pet_name})."
                )
        return warnings

    def mark_task_complete(self, task_id: int, completed_on: date | None = None) -> Task | None:
        """Complete a task and create its next daily or weekly occurrence."""
        task = next((item for item in self.tasks if item.task_id == task_id), None)
        if task is None:
            raise ValueError(f"No task found with id {task_id}")

        task.mark_complete()
        if task.frequency == "none":
            return None

        interval = timedelta(days=1 if task.frequency == "daily" else 7)
        next_due_date = (completed_on or date.today()) + interval
        next_task = Task(
            title=task.title,
            pet_name=task.pet_name,
            time=task.time,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            due_date=next_due_date,
            frequency=task.frequency,
        )
        self.add_task(next_task)
        return next_task

    def save_to_json(self, path: str | Path, owner: Owner | None = None) -> None:
        """Save owner, pets, and tasks as readable JSON."""
        selected_owner = owner or self.owner
        payload = {
            "owner": {
                "name": selected_owner.name if selected_owner else "",
                "pets": [
                    {"name": pet.name, "species": pet.species}
                    for pet in selected_owner.pets
                ] if selected_owner else [],
            },
            "tasks": [
                {
                    "task_id": task.task_id,
                    "title": task.title,
                    "pet_name": task.pet_name,
                    "time": task.time,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                    "due_date": task.due_date.isoformat(),
                    "frequency": task.frequency,
                    "completed": task.completed,
                }
                for task in self.tasks
            ],
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load_from_json(cls, path: str | Path) -> tuple[Owner, Scheduler]:
        """Load an owner and scheduler from a JSON file."""
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        owner_data = payload["owner"]
        owner = Owner(
            name=owner_data["name"],
            pets=[Pet(name=item["name"], species=item["species"]) for item in owner_data["pets"]],
        )
        scheduler = cls(owner)
        loaded_tasks = [
            Task(
                task_id=item["task_id"],
                title=item["title"],
                pet_name=item["pet_name"],
                time=item["time"],
                duration_minutes=item["duration_minutes"],
                priority=item["priority"],
                due_date=date.fromisoformat(item["due_date"]),
                frequency=item["frequency"],
                completed=item["completed"],
            )
            for item in payload["tasks"]
        ]
        for task in loaded_tasks:
            scheduler.add_task(task)
        if loaded_tasks:
            _set_next_task_id(max(task.task_id for task in loaded_tasks) + 1)
        return owner, scheduler