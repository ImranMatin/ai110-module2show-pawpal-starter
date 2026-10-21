from datetime import date

from pawpal_system import Scheduler, Task


def main() -> None:
    scheduler = Scheduler()
    scheduler.add_task(Task("Evening walk", "Mochi", "18:00", 30, "medium"))
    scheduler.add_task(Task("Morning medicine", "Mochi", "08:00", 5, "high", frequency="daily"))
    scheduler.add_task(Task("Breakfast", "Biscuit", "08:00", 10, "high"))

    print("PawPal+ daily schedule")
    for task in scheduler.sort_by_time():
        print(f"{task.time} - {task.title} for {task.pet_name} ({task.duration_minutes} min)")

    print("\nConflict warnings")
    for warning in scheduler.detect_conflicts():
        print(f"WARNING: {warning}")

    recurring_task = next(
        task
        for task in scheduler.filter_tasks(pet_name="Mochi", completed=False)
        if task.frequency == "daily"
    )
    next_task = scheduler.mark_task_complete(recurring_task.task_id, date.today())
    print(f"\nNext medicine due: {next_task.due_date.isoformat()}")


if __name__ == "__main__":
    main()