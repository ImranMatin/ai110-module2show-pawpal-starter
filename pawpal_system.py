from dataclasses import dataclass, field
from datetime import date, timedelta
from itertools import count


_task_ids = count(1)


@dataclass
class Pet:
    """A pet whose care tasks can be scheduled."""

    name: str
    species: str


@dataclass
class Owner:
    """An owner and the pets they care for."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's household."""
        self.pets.append(pet)


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
        if self.frequency not in {"none", "daily", "weekly"}:
            raise ValueError("frequency must be none, daily, or weekly")


class Scheduler:
    """Store tasks and provide simple sorting, filtering, and recurrence logic."""

    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule."""
        self.tasks.append(task)

    def sort_by_time(self, tasks: list[Task] | None = None) -> list[Task]:
        """Return tasks in chronological HH:MM order without mutating input."""
        return sorted(tasks if tasks is not None else self.tasks, key=lambda task: task.time)

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

        task.completed = True
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