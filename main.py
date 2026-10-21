from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan", [Pet("Mochi", "dog"), Pet("Biscuit", "cat")])
    scheduler = Scheduler(owner)
    scheduler.add_task(
        Task("Evening walk", "Mochi", "18:00", 30, "medium", due_date=date(2026, 10, 21))
    )
    scheduler.add_task(
        Task(
            "Morning medicine",
            "Mochi",
            "08:00",
            5,
            "high",
            due_date=date(2026, 10, 21),
            frequency="daily",
        )
    )
    scheduler.add_task(
        Task("Breakfast", "Biscuit", "08:00", 10, "high", due_date=date(2026, 10, 21))
    )

    print(f"PawPal+ schedule for {owner.name}")
    print("Priority order (high to low, then time)")
    priority_icons = {"high": "!", "medium": "-", "low": "."}
    for task in scheduler.sort_by_priority():
        print(
            f"{priority_icons[task.priority]} [{task.priority.upper():6}] {task.time} "
            f"{task.title} - {task.pet_name} ({task.duration_minutes} min)"
        )

    print("\nConflict warnings")
    for warning in scheduler.detect_conflicts():
        print(f"WARNING: {warning}")

    next_slot = scheduler.next_available_slot(date(2026, 10, 21), 30)
    print(f"\nNext 30-minute available slot: {next_slot}")

    recurring_task = next(task for task in scheduler.tasks if task.frequency == "daily")
    next_task = scheduler.mark_task_complete(recurring_task.task_id, date(2026, 10, 21))
    print(f"\nNext medicine due: {next_task.due_date.isoformat()}")


if __name__ == "__main__":
    main()