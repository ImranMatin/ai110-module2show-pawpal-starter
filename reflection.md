# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The final model has four main classes. `Owner` represents the person using the planner and owns a list of `Pet` objects. `Pet` stores a pet's name and species. `Task` stores its pet, time, duration, priority, due date, completion state, and recurrence frequency. `Scheduler` owns the tasks and handles sorting, filtering, conflict checks, and completion.

**b. Design changes**

The scheduling methods live on `Scheduler` rather than being spread across the UI or individual pets. That keeps `app.py` focused on collecting input and displaying results, while the same behavior can be exercised from the CLI demo and pytest.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler orders tasks by their 24-hour `HH:MM` value and can filter by pet and completion state. Tasks also retain duration and priority for display. Daily and weekly frequency controls what gets created after completion.

**b. Tradeoffs**

Conflict detection checks exact matching start times on the same date instead of overlapping duration ranges. It ignores completed tasks in the UI. This keeps the algorithm easy to explain and gives a useful warning for obvious collisions, but it can miss a 30-minute task that overlaps a task starting 15 minutes later. A future improvement would compare each task's start and end times on the same due date.

## 3. AI Collaboration

**a. How I used AI**

I used the coding assistant to translate the project requirements into a small model, generate the initial method/test structure, and help connect Streamlit inputs to Python objects. Asking for concrete examples of `sorted(..., key=lambda task: task.time)` and `timedelta` recurrence made the intended behavior easier to check.

The workflow was divided into implementation, testing, and UI/documentation phases by the prompts and review steps. I did not actually open separate chat sessions, so the separation was organizational rather than a feature of the chat tool.

**b. Judgment and verification**

I kept conflict detection limited to exact start-time matches rather than adding a more complicated interval algorithm before the project required it. I documented that limitation instead of implying it catches every overlap. I verified the methods with six tests and ran the CLI demo rather than relying only on generated code.

## 4. Testing and Verification

**a. What I tested**

The seven tests cover chronological order, case-insensitive pet filtering, completion filtering, daily recurrence, weekly recurrence, duplicate-time warnings across pets, different-date non-conflicts, and empty schedules. These checks cover the main behaviors and a few boundary cases without depending on Streamlit rendering.

**b. Confidence**

My confidence is 4 out of 5 for these covered behaviors. I would next test invalid time input, duplicate pet names, conflicts on different dates, and overlapping task durations. I would also add an automated test for the UI's session-state workflow.

## 5. Reflection

**a. What went well**

Keeping the scheduling rules in a plain Python class made them usable in both the Streamlit app and the terminal demo. The same methods are directly testable without clicking through the interface.

**b. What I would improve**

I would add persistence beyond the current Streamlit session and detect duration-based overlaps. I would also provide task editing and deletion so owners can correct a plan without restarting their session.

**c. Key takeaway**

Being the lead architect means setting boundaries, checking assumptions, and verifying the result. AI can accelerate drafts, but I still need to decide what the algorithm promises, what it leaves out, and whether tests prove the behavior users will see.
