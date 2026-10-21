# PawPal+

PawPal+ is a small pet-care scheduler with a Streamlit interface and a Python scheduling layer. It keeps an owner's pets and tasks in Streamlit session state, so they remain available across reruns in the same session.

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
- `Scheduler.sort_by_time()` returns tasks in chronological `HH:MM` order.
- `Scheduler.filter_tasks()` filters by pet name, completion status, or both.
- `Scheduler.detect_conflicts()` returns helpful warning strings for incomplete tasks with the same exact scheduled time on the same date. The UI displays those with `st.warning` and lists the affected task names and pets.
- `Scheduler.mark_task_complete()` marks a task complete and creates its next daily or weekly occurrence using `timedelta`.
- `Owner.add_pet()` keeps pet ownership in the model; `app.py` stores the `Owner` and `Scheduler` instances in `st.session_state`.

## Testing PawPal+

Run the automated suite:

```bash
python -m pytest
```

Tests cover chronological sorting, pet/status filters, daily and weekly recurrence, duplicate-time conflict warnings (including across pets), date-scoped conflicts, and the empty-schedule case.

Latest test run:

```text
tests/test_pawpal.py .......                                             [100%]

============================== 7 passed in 0.02s ===============================
```

Confidence level: **4/5** for the tested scheduling behaviors. The suite is intentionally focused; exact-time checking does not yet model duration overlap, and persistence is limited to a Streamlit session rather than a database.

## Demo Walkthrough

1. Enter or keep the owner name, then add one or more pets with their species.
2. Add care tasks by choosing a pet, time, duration, priority, and repeat frequency.
3. Review tasks in chronological order. Use the pet and completion controls to narrow the displayed list.
4. If two incomplete tasks on the same date share an exact time, PawPal+ shows a warning naming both tasks and pets so the owner can adjust a time.
5. Mark a task complete. A daily or weekly task creates its next occurrence; a one-time task is simply marked complete.

The terminal demo (`python main.py`) also creates tasks out of order, prints the sorted schedule and conflict warning, filters Mochi's tasks, and shows the next recurrence date.

```text
PawPal+ daily schedule
08:00 - Morning medicine for Mochi (5 min)
08:00 - Breakfast for Biscuit (10 min)
18:00 - Evening walk for Mochi (30 min)

Conflict warnings
WARNING: 2026-10-21 08:00: Morning medicine (Mochi) conflicts with Breakfast (Biscuit).

Next medicine due: 2026-10-22
```

## Architecture

See [the final UML source](diagrams/uml_final.mmd) for the class relationships and scheduler methods.
