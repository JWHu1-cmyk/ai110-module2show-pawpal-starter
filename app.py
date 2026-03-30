import streamlit as st
from pawpal_system import CareTask, Pet, Owner, Planner

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

# --- Session state initialization ---
# These objects persist across Streamlit reruns so data isn't lost on every click.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes_per_day=60)

if "pet" not in st.session_state:
    pet = Pet(name="Mochi", species="dog")
    st.session_state.owner.add_pet(pet)
    st.session_state.pet = pet

if "planner" not in st.session_state:
    st.session_state.planner = Planner()

st.divider()

# --- Owner & Pet info ---
st.subheader("Owner & Pet Info")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
available_minutes = st.number_input(
    "Available minutes per day", min_value=1, max_value=480,
    value=st.session_state.owner.available_minutes_per_day
)
st.session_state.owner.update_profile(name=owner_name, available_minutes=int(available_minutes))

pet_name = st.text_input("Pet name", value=st.session_state.pet.name)
species = st.selectbox("Species", ["dog", "cat", "other"],
                        index=["dog", "cat", "other"].index(st.session_state.pet.species))
st.session_state.pet.name = pet_name
st.session_state.pet.species = species

# --- Tasks ---
st.markdown("### Tasks")
PRIORITY_MAP = {"low": 1, "medium": 3, "high": 5}

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    new_task = CareTask(
        title=task_title,
        category="General",
        duration_minutes=int(duration),
        priority=PRIORITY_MAP[priority_label],
    )
    st.session_state.pet.add_care_task(new_task)

tasks = st.session_state.pet.list_tasks()
if tasks:
    st.write("Current tasks:")
    st.table([
        {"Title": t.title, "Duration": f"{t.duration_minutes} min",
         "Priority": t.priority, "Done": t.completed}
        for t in tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

# --- Schedule ---
st.divider()
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    plan = st.session_state.planner.build_daily_plan(
        st.session_state.owner, st.session_state.pet
    )
    explanation = st.session_state.planner.explain_plan(plan)
    st.success("Schedule generated!")
    st.text(explanation)
