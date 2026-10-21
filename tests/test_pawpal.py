from datetime import date

from pawpal_system import Scheduler, Task


def test_sort_by_time_returns_chronological_order():
    scheduler = Scheduler()
    late = Task("Evening walk", "Mochi", "19:00")
    early = Task("Breakfast", "Mochi", "07:30")
    midday = Task("Medication", "Mochi", "12:15")
    for task in (late, early, midday):
        scheduler.add_task(task)

    assert scheduler.sort_by_time() == [early, midday, late]


def test_filter_by_pet_and_completion_state():
    scheduler = Scheduler()
    mochi_task = Task("Walk", "Mochi", "08:00", completed=True)
    biscuit_task = Task("Feeding", "Biscuit", "08:30")
    scheduler.add_task(mochi_task)
    scheduler.add_task(biscuit_task)

    assert scheduler.filter_tasks(pet_name="mochi") == [mochi_task]
    assert scheduler.filter_tasks(completed=False) == [biscuit_task]
    assert scheduler.filter_tasks(pet_name="Mochi", completed=True) == [mochi_task]


def test_completing_daily_task_creates_next_day_occurrence():
    scheduler = Scheduler()
    task = Task("Medicine", "Mochi", "09:00", frequency="daily")
    scheduler.add_task(task)

    next_task = scheduler.mark_task_complete(task.task_id, date(2026, 10, 21))

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == date(2026, 10, 22)
    assert next_task.completed is False
    assert next_task in scheduler.tasks


def test_completing_weekly_task_creates_occurrence_seven_days_later():
    scheduler = Scheduler()
    task = Task("Grooming", "Biscuit", "10:00", frequency="weekly")
    scheduler.add_task(task)

    next_task = scheduler.mark_task_complete(task.task_id, date(2026, 10, 21))

    assert next_task is not None
    assert next_task.due_date == date(2026, 10, 28)


def test_exact_time_conflicts_are_reported_as_warnings():
    scheduler = Scheduler()
    scheduler.add_task(Task("Walk", "Mochi", "08:00"))
    scheduler.add_task(Task("Feeding", "Biscuit", "08:00"))
    scheduler.add_task(Task("Nap", "Mochi", "09:00"))

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "Walk (Mochi)" in warnings[0]
    assert "Feeding (Biscuit)" in warnings[0]


def test_tasks_at_same_time_on_different_dates_do_not_conflict():
    scheduler = Scheduler()
    scheduler.add_task(Task("Walk", "Mochi", "08:00", due_date=date(2026, 10, 21)))
    scheduler.add_task(Task("Walk", "Mochi", "08:00", due_date=date(2026, 10, 22)))

    assert scheduler.detect_conflicts() == []


def test_empty_scheduler_has_no_tasks_or_conflicts():
    scheduler = Scheduler()

    assert scheduler.sort_by_time() == []
    assert scheduler.filter_tasks() == []
    assert scheduler.detect_conflicts() == []