import streamlit as st
from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", [Pet("Mochi", "dog")])
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler
owner.name = st.text_input("Owner name", value=owner.name)

with st.expander("Add a pet"):
    with st.form("pet_form"):
        new_pet_name = st.text_input("Pet name")
        new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])
        pet_submitted = st.form_submit_button("Add pet")
    if pet_submitted:
        if not new_pet_name.strip():
            st.warning("Enter a name for the pet.")
        elif any(pet.name.casefold() == new_pet_name.strip().casefold() for pet in owner.pets):
            st.warning("A pet with that name is already in this household.")
        else:
            owner.add_pet(Pet(new_pet_name.strip(), new_pet_species))
            st.success(f"Added {new_pet_name.strip()}.")

st.subheader("Schedule a care task")
if not owner.pets:
    st.info("Add a pet before scheduling a task.")
else:
    pet_names = [pet.name for pet in owner.pets]
    with st.form("task_form"):
        task_title = st.text_input("Task")
        col1, col2, col3 = st.columns(3)
        with col1:
            pet_name = st.selectbox("Pet", pet_names)
        with col2:
            task_time = st.time_input("Time")
        with col3:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
        frequency = st.selectbox("Repeat", ["none", "daily", "weekly"])
        task_submitted = st.form_submit_button("Add task")
    if task_submitted:
        if not task_title.strip():
            st.warning("Enter a task description.")
        else:
            scheduler.add_task(
                Task(
                    title=task_title.strip(),
                    pet_name=pet_name,
                    time=task_time.strftime("%H:%M"),
                    duration_minutes=int(duration),
                    priority=priority,
                    due_date=date.today(),
                    frequency=frequency,
                )
            )
            st.success(f"Scheduled {task_title.strip()} for {pet_name}.")

st.subheader("Tasks")
pet_filter = st.selectbox("Filter by pet", ["All pets", *[pet.name for pet in owner.pets]])
status_filter = st.selectbox("Completion", ["All", "To do", "Completed"])
filtered_tasks = scheduler.filter_tasks(
    pet_name=None if pet_filter == "All pets" else pet_filter,
    completed={"All": None, "To do": False, "Completed": True}[status_filter],
)
visible_tasks = scheduler.sort_by_time(filtered_tasks)
if visible_tasks:
    st.table(
        [
            {
                "Time": task.time,
                "Task": task.title,
                "Pet": task.pet_name,
                "Duration": f"{task.duration_minutes} min",
                "Priority": task.priority,
                "Due": task.due_date.isoformat(),
                "Repeat": task.frequency,
                "Status": "Done" if task.completed else "To do",
            }
            for task in visible_tasks
        ]
    )
else:
    st.info("No tasks match these filters yet.")

conflicts = scheduler.detect_conflicts([task for task in filtered_tasks if not task.completed])
if conflicts:
    st.warning("Scheduling conflicts found. Adjust one of these tasks to avoid overlap:")
    for warning in conflicts:
        st.write(f"- {warning}")
elif visible_tasks:
    st.success("No exact-time conflicts in the filtered schedule.")

incomplete_tasks = scheduler.filter_tasks(completed=False)
if incomplete_tasks:
    task_options = {f"{task.time} · {task.title} ({task.pet_name})": task.task_id for task in incomplete_tasks}
    selected_label = st.selectbox("Mark a task complete", list(task_options))
    if st.button("Complete task"):
        next_task = scheduler.mark_task_complete(task_options[selected_label])
        if next_task:
            st.success(f"Completed. Next {next_task.frequency} task is due {next_task.due_date.isoformat()}.")
        else:
            st.success("Task marked complete.")
