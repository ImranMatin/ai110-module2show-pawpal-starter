# PawPal+

PawPal+ is a small pet-care scheduler with a Streamlit interface and a Python scheduling layer. Owners have pets, pets own their care tasks, and a scheduler coordinates tasks across the household. The app persists owner, pet, and task data in `data.json` between runs.

## Run the app

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run the terminal demonstration with `python main.py`.

## Features

- Add pets and care tasks with time, duration, priority, and recurrence.
- `Scheduler.sort_by_time()` returns tasks in chronological `HH:MM` order; `Scheduler.sort_by_priority()` orders high, medium, then low priority, with date and time as tie-breakers.
- `Scheduler.filter_tasks()` filters by pet name, completion status, or both.
- `Scheduler.detect_conflicts()` returns helpful warning strings for incomplete tasks with the same exact scheduled time on the same date. The UI displays those with `st.warning` and lists the affected task names and pets.
- `Scheduler.mark_task_complete()` marks a task complete and creates its next daily or weekly occurrence using `timedelta`.
- `Scheduler.next_available_slot()` finds the earliest duration-safe opening within a chosen daily window.
- `Owner.add_pet()` and `Owner.add_task()` maintain the household model; `Pet.add_task()` and `Pet.list_tasks()` manage each pet's own tasks.
- `Scheduler.save_to_json()` and `Scheduler.load_from_json()` serialize the owner, pets, and tasks to/from JSON. The Streamlit app loads `data.json` on a new session and saves after owner, pet, task, and completion changes. The file is created beside `app.py` when a change is first saved.
- The UI uses `st.table`, `st.success`, and `st.warning` for structured schedule data and feedback. The CLI demo uses simple text priority markers (`!`, `-`, `.`) and labels instead of an extra formatting dependency.

Persistence changes are in `pawpal_system.py` (JSON conversion) and `app.py` (load/save workflow); tests use pytest's temporary directory fixture so they do not alter the app's `data.json`.

## Testing PawPal+

Run the automated suite:

```bash
python -m pytest
```

Tests cover chronological sorting, priority ordering, pet/status filters, daily and weekly recurrence, duplicate-time conflict warnings (including across pets), date-scoped conflicts, empty schedules, multi-pet task ownership, duration-safe slot search, and JSON round-tripping.

Latest test run:

```text
tests/test_pawpal.py ............                                        [100%]

============================== 12 passed in 0.03s ==============================
```

Confidence level: **4/5** for the tested scheduling behaviors. Conflict warnings still detect exact matching start times rather than every duration overlap; `next_available_slot()` separately accounts for durations when finding an opening. JSON persistence is local-file storage, not a multi-user database.

## Demo Walkthrough

https://www.loom.com/share/76511f8943684351b600c1bee01ce740

<div style="position: relative; padding-bottom: 62.5%; height: 0;"><iframe src="https://www.loom.com/embed/76511f8943684351b600c1bee01ce740" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

1. Enter or keep the owner name, then add one or more pets with their species.
2. Add care tasks by choosing a pet, time, duration, priority, and repeat frequency.
3. Review tasks by time or priority. Use the pet and completion controls to narrow the displayed list.
4. If two incomplete tasks on the same date share an exact time, PawPal+ shows a warning naming both tasks and pets so the owner can adjust a time.
5. Ask for the next available slot for a duration, then mark a task complete. A daily or weekly task creates its next occurrence; a one-time task is simply marked complete. Changes are saved in `data.json` and loaded on a later app run.

The terminal demo (`python main.py`) creates an owner with two pets and tasks entered out of order, then prints the priority schedule, conflict warning, next available time, and recurrence date.

```text
PawPal+ schedule for Jordan
Priority order (high to low, then time)
! [HIGH  ] 08:00 Morning medicine - Mochi (5 min)
! [HIGH  ] 08:00 Breakfast - Biscuit (10 min)
- [MEDIUM] 18:00 Evening walk - Mochi (30 min)

Conflict warnings
WARNING: 2026-10-21 08:00: Morning medicine (Mochi) conflicts with Breakfast (Biscuit).

Next 30-minute available slot: 07:00

Next medicine due: 2026-10-22
```

## Architecture

See [the final UML source](diagrams/uml_final.mmd) for the class relationships and scheduler methods.
