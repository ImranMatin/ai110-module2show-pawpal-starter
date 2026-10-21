# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked GitHub Copilot to close gaps identified against the project rubric and add persistence plus smarter scheduling: owner/pet task relationships, priority ordering, duration-aware next-slot search, JSON save/load, a matching UI, and tests.

**What did the agent do?**

It updated `pawpal_system.py`, `app.py`, `main.py`, `tests/test_pawpal.py`, `diagrams/uml_final.mmd`, `README.md`, `reflection.md`, `.gitignore`, and this log. It implemented the model relationships, JSON persistence, priority/time sorting, next-slot search, a two-pet CLI example, and tests. It ran `python -m pytest` during development and caught a CLI demo selection mistake before correcting it.

**What did you have to verify or fix manually?**

The demo and tests were rerun after the changes. The first demo run showed that the recurrence example selected a one-time task; the selection was narrowed to the daily task. A later test exposed the exact behavior of overlapping busy intervals, and the slot search is verified to move to the end of the combined busy period. I also checked that conflict warnings are date-scoped and that generated `data.json` is ignored so personal app data is not committed. Conflict warnings still use exact-time matching; the separate slot search accounts for durations.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

|                       | Option A                                                                          | Option B                                                                                                                                               |
| --------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Model / tool used** | GitHub Copilot, broad feature prompt                                              | GitHub Copilot, rubric checklist followed by a targeted gap-fix request                                                                                |
| **Prompt**            | Add stretch features such as persistence, priority scheduling, and better output. | Compare the repository against the explicit class, demo, test, documentation, and stretch criteria; then include the missing items.                    |
| **Response summary**  | Identified the feature direction and produced an implementation plan.             | Found concrete omissions: Pet task ownership, Owner/two-Pet demo setup, real persistence, and empty AI documentation; changes were then tied to tests. |
| **What was useful**   | Encouraged adding meaningful capabilities beyond the minimum scheduler.           | Made completion criteria observable and exposed gaps that a feature brainstorm alone did not catch.                                                    |
| **Problems noticed**  | A broad feature request can leave rubric details implicit.                        | A checklist can encourage scope growth, so each addition still needed a test and a clear limitation.                                                   |
| **Decision**          | Useful for ideation, not sufficient as the final acceptance check.                | Used the rubric-oriented approach to guide implementation and verification.                                                                            |

Both approaches were prompts to the same assistant, not a comparison between two AI models. The broad prompt helped choose useful extensions; the rubric-focused prompt gave a better completion check. The final implementation followed the rubric-oriented approach and verified its behavior through tests and the CLI demo.
