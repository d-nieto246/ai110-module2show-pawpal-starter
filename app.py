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
    st.table([{"name": pet.name, "species": pet.species, "tasks": len(pet.get_tasks())} for pet in pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Schedule a Task")
st.caption("Submitting this form calls Pet.add_task(...) and Scheduler.add_entry(...).")

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
            st.session_state["scheduler"].add_entry(selected_pet, task, scheduled_at)
            st.success(
                f"Scheduled {task.type} for {selected_pet.name} at {scheduled_at.strftime('%Y-%m-%d %I:%M %p')}."
            )

    entries = st.session_state["scheduler"].view_scheduler()
    if entries:
        st.write("Current schedule:")
        st.table(
            [
                {
                    "date": entry[2].strftime("%Y-%m-%d"),
                    "time": entry[2].strftime("%I:%M %p"),
                    "pet": entry[0].name,
                    "species": entry[0].species,
                    "task": entry[1].type,
                    "description": entry[1].description,
                    "frequency": entry[1].frequency,
                }
                for entry in entries
            ]
        )
    else:
        st.info("No scheduled tasks yet.")
else:
    st.info("Add at least one pet before scheduling tasks.")
