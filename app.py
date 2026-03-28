import streamlit as st
from datetime import datetime, time

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

# Persist core domain objects in the session-state "vault".
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(name=owner_name)
else:
    st.session_state["owner"].name = owner_name

if "scheduler" not in st.session_state:
    st.session_state["scheduler"] = Scheduler(owner=st.session_state["owner"])
else:
    st.session_state["scheduler"].owner = st.session_state["owner"]

st.caption(f"Session owner loaded: {st.session_state['owner'].name}")

st.markdown("### Add Pet")
st.caption("Submitting this form calls Owner.add_pet(...).")

with st.form("add_pet_form", clear_on_submit=True):
    new_pet_name = st.text_input("Pet name", value="")
    new_pet_species = st.selectbox("Species", ["dog", "cat", "bird", "fish", "other"])
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    clean_name = new_pet_name.strip()
    if not clean_name:
        st.error("Please enter a pet name.")
    elif st.session_state["owner"].get_pet_by_name(clean_name):
        st.warning("A pet with that name already exists.")
    else:
        st.session_state["owner"].add_pet(Pet(name=clean_name, species=new_pet_species))
        st.success(f"Added {clean_name} to {st.session_state['owner'].name}.")

pets = st.session_state["owner"].get_pets()
if pets:
    st.write("Current pets:")
    st.dataframe(
        [
            {
                "Pet #": index,
                "Name": pet.name,
                "Species": pet.species,
                "Tasks": len(pet.get_tasks()),
            }
            for index, pet in enumerate(pets, start=1)
        ],
        hide_index=True,
        use_container_width=True,
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Schedule a Task")
st.caption("Submitting this form calls Pet.add_task(...) and Scheduler.add_entry_with_warning(...).")

if pets:
    pet_options = {f"{pet.name} ({pet.species})": pet for pet in pets}
    with st.form("schedule_task_form", clear_on_submit=True):
        selected_pet_label = st.selectbox("Select pet", list(pet_options.keys()))
        task_type = st.text_input("Task type", value="Feeding")
        task_description = st.text_input("Task description", value="Morning meal")
        task_frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"], index=0)
        task_date = st.date_input("Task date")
        task_time = st.time_input("Task time", value=time(8, 0))
        schedule_task_submitted = st.form_submit_button("Add and schedule task")

    if schedule_task_submitted:
        clean_type = task_type.strip()
        clean_description = task_description.strip()
        if not clean_type or not clean_description:
            st.error("Task type and description are required.")
        else:
            selected_pet = pet_options[selected_pet_label]
            task = Task(type=clean_type, description=clean_description, frequency=task_frequency)
            selected_pet.add_task(task)
            scheduled_at = datetime.combine(task_date, task_time)
            added_entry, warning = st.session_state["scheduler"].add_entry_with_warning(
                selected_pet,
                task,
                scheduled_at,
            )
            st.success(
                f"Scheduled {added_entry[1].type} for {added_entry[0].name} at {added_entry[2].strftime('%Y-%m-%d %I:%M %p')}."
            )
            if warning:
                st.warning(warning)

    entries = st.session_state["scheduler"].view_scheduler()
    if entries:
        scheduler = st.session_state["scheduler"]
        all_tasks = scheduler.get_all_tasks()
        pending_tasks = scheduler.get_pending_tasks()
        conflicts = scheduler.detect_time_conflicts()

        st.markdown("#### Schedule Dashboard")
        metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
        metric_col_1.success(f"Scheduled entries: {len(entries)}")
        metric_col_2.info(f"Pending tasks: {len(pending_tasks)} / {len(all_tasks)}")
        if conflicts:
            metric_col_3.warning(f"Conflicts: {len(conflicts)}")
        else:
            metric_col_3.success("Conflicts: 0")

        st.markdown("#### Current schedule (sorted)")
        st.dataframe(
            [
                {
                    "Task #": index,
                    "date": entry[2].strftime("%Y-%m-%d"),
                    "time": entry[2].strftime("%I:%M %p"),
                    "pet": entry[0].name,
                    "species": entry[0].species,
                    "task": entry[1].type,
                    "description": entry[1].description,
                    "frequency": entry[1].frequency,
                }
                for index, entry in enumerate(entries, start=1)
            ],
            hide_index=True,
            use_container_width=True,
        )

        st.markdown("#### Filtered task view")
        filter_col_1, filter_col_2 = st.columns(2)
        pet_filter_options = ["All pets"] + [pet.name for pet in pets]
        selected_pet_filter = filter_col_1.selectbox(
            "Filter by pet",
            pet_filter_options,
            key="filter_by_pet",
        )
        selected_status_filter = filter_col_2.selectbox(
            "Filter by status",
            ["All", "Pending", "Completed"],
            key="filter_by_status",
        )

        completed_filter = None
        if selected_status_filter == "Pending":
            completed_filter = False
        elif selected_status_filter == "Completed":
            completed_filter = True

        pet_name_filter = None if selected_pet_filter == "All pets" else selected_pet_filter
        filtered_tasks = scheduler.filter_tasks(completed=completed_filter, pet_name=pet_name_filter)

        if filtered_tasks:
            st.dataframe(
                [
                    {
                        "Task #": index,
                        "pet": task.pet.name if task.pet is not None else "Unknown",
                        "task": task.type,
                        "description": task.description,
                        "frequency": task.frequency,
                        "status": "Completed" if task.completed else "Pending",
                    }
                    for index, task in enumerate(filtered_tasks, start=1)
                ],
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info("No tasks match your current filters.")

        if conflicts:
            st.warning(
                f"{len(conflicts)} scheduling conflict(s) found. Consider shifting one task by 15-30 minutes to reduce stress for you and your pet."
            )
            with st.expander("View conflict details"):
                st.table(
                    [
                        {
                            "time": conflict[0][2].strftime("%Y-%m-%d %I:%M %p"),
                            "entry_1": f"{conflict[0][0].name} - {conflict[0][1].type}",
                            "entry_2": f"{conflict[1][0].name} - {conflict[1][1].type}",
                        }
                        for conflict in sorted(conflicts, key=lambda pair: pair[0][2])
                    ]
                )
        else:
            st.success("No overlapping schedule times detected. Great job spacing tasks out.")
    else:
        st.info("No scheduled tasks yet.")
else:
    st.info("Add at least one pet before scheduling tasks.")
