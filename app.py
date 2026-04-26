# streamlit run app.py

import streamlit as st
import pandas as pd
from pawpal_system import Owner, Pet, Task, Scheduler
from agent import suggest_tasks

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ── Session state ─────────────────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=90)

owner: Owner = st.session_state.owner
pets = owner.get_pets()

st.title("🐾 PawPal+")
st.caption(f"Owner: **{owner.name}** · {owner.available_minutes} min available today")

st.divider()

# ── Add a Pet ─────────────────────────────────────────────────────────────────
st.subheader("Add a Pet")
col1, col2, col3, col4 = st.columns(4)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])
with col3:
    breed = st.text_input("Breed (optional)", value="")
with col4:
    age = st.number_input("Age", min_value=0, max_value=30, value=2)

if st.button("Add Pet + AI Suggestions"):
    existing = [p.name for p in pets]
    if pet_name in existing:
        st.warning(f"{pet_name} is already added.")
    else:
        owner.add_pet(Pet(name=pet_name, species=species, breed=breed, age=int(age)))
        with st.spinner("Generating care tasks with AI..."):
            try:
                suggestions = suggest_tasks(pet_name, species, breed, int(age))
                st.session_state.ai_suggestions = suggestions
                st.session_state.suggestions_for = pet_name
                st.rerun()
            except Exception as e:
                st.session_state.ai_suggestions = None
                st.error(f"AI suggestions failed: {e}")

if pets:
    st.write("**Registered pets:**", ", ".join(p.name for p in pets))

# ── AI Task Suggestions confirmation ─────────────────────────────────────────
if st.session_state.get("ai_suggestions") and st.session_state.get("suggestions_for"):
    pet_for = st.session_state.suggestions_for
    suggestions = st.session_state.ai_suggestions

    st.subheader(f"AI Suggested Tasks for {pet_for}")
    st.info("Uncheck any tasks you don't want, then click **Confirm Selected Tasks**.")

    df = pd.DataFrame([{
        "Add": True,
        "Task": t["name"],
        "Category": t["category"],
        "Duration (min)": t["duration_minutes"],
        "Priority": t["priority"],
        "Time": t["time"],
        "Recurring": "Yes" if t["recurring"] else "No",
        "Every N days": t["interval_days"],
    } for t in suggestions])

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={"Add": st.column_config.CheckboxColumn("Add", default=True)},
        disabled=["Task", "Category", "Duration (min)", "Priority", "Time", "Recurring", "Every N days"],
    )

    selected = [suggestions[i] for i, row in edited_df.iterrows() if row["Add"]]

    col_confirm, col_skip = st.columns(2)
    with col_confirm:
        if st.button("Confirm Selected Tasks", type="primary"):
            pet_obj = next((p for p in pets if p.name == pet_for), None)
            if pet_obj and selected:
                for t in selected:
                    pet_obj.add_task(Task(
                        name=t["name"],
                        category=t["category"],
                        duration_minutes=t["duration_minutes"],
                        priority=t["priority"],
                        time=t["time"],
                        recurring=t["recurring"],
                        interval_days=t["interval_days"],
                    ))
            st.session_state.ai_suggestions = None
            st.session_state.suggestions_for = None
            st.success(f"Added {len(selected)} task(s) to {pet_for}!")
            st.rerun()
    with col_skip:
        if st.button("Skip"):
            st.session_state.ai_suggestions = None
            st.session_state.suggestions_for = None
            st.rerun()

st.divider()

# ── Add a Task ────────────────────────────────────────────────────────────────
st.subheader("Add a Task")
if not pets:
    st.info("Add a pet first before scheduling tasks.")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        target_pet = st.selectbox("For pet", [p.name for p in pets])
    with col2:
        task_title = st.text_input("Task name", value="Morning walk")
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.slider("Priority (1–5)", min_value=1, max_value=5, value=3)

    col5, col6, col7 = st.columns(3)
    with col5:
        task_time = st.text_input("Time (HH:MM)", value="09:00",
                                   help="Leave as 00:00 if time is not set")
    with col6:
        recurring = st.checkbox("Recurring?")
    with col7:
        interval_days = st.number_input("Every N days", min_value=1, max_value=365, value=1,
                                         disabled=not recurring)

    if st.button("Add Task"):
        pet_obj = next(p for p in pets if p.name == target_pet)
        pet_obj.add_task(Task(
            name=task_title,
            category="General",
            duration_minutes=int(duration),
            priority=priority,
            time=task_time,
            recurring=recurring,
            interval_days=int(interval_days),
        ))
        st.success(f"Added '{task_title}' to {target_pet}.")
        st.rerun()

st.divider()

# ── Conflict Warnings ─────────────────────────────────────────────────────────
if pets:
    scheduler = Scheduler(owner)
    warnings = scheduler.get_conflict_warnings()
    if warnings:
        st.subheader("⚠️ Schedule Conflicts")
        for w in warnings:
            st.warning(w)
        st.divider()

# ── Task View: Sorted + Filtered ──────────────────────────────────────────────
if pets and any(p.get_tasks() for p in pets):
    st.subheader("All Tasks")

    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        filter_pet = st.selectbox(
            "Filter by pet",
            ["All pets"] + [p.name for p in pets],
        )
    with col_filter2:
        filter_status = st.selectbox(
            "Filter by status",
            ["All", "Pending only", "Completed only"],
        )

    scheduler = Scheduler(owner)

    pet_name_filter = None if filter_pet == "All pets" else filter_pet
    completed_filter = None
    if filter_status == "Pending only":
        completed_filter = False
    elif filter_status == "Completed only":
        completed_filter = True

    filtered = scheduler.filter_tasks(pet_name=pet_name_filter, completed=completed_filter)
    sorted_tasks = sorted(filtered, key=lambda t: t.time)

    if not sorted_tasks:
        st.info("No tasks match the selected filters.")
    else:
        rows = []
        for t in sorted_tasks:
            rows.append({
                "Time": t.time,
                "Task": t.name,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
                "Recurring": "Yes" if t.recurring else "No",
                "Status": "Done" if t.completed else "Pending",
            })
        st.table(rows)

    st.divider()

# ── Generate Schedule ─────────────────────────────────────────────────────────
st.subheader("Today's Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()
    if not plan:
        st.warning("No tasks fit within the available time, or no tasks have been added yet.")
    else:
        total = sum(t.duration_minutes for t in plan)
        remaining = owner.available_minutes - total
        st.success(f"Scheduled **{len(plan)} task(s)** · {total} min used · {remaining} min remaining")

        rows = []
        for t in plan:
            rows.append({
                "Time": t.time,
                "Task": t.name,
                "Category": t.category,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
                "High Priority": "Yes" if t.is_high_priority() else "No",
                "Recurring": "Yes" if t.recurring else "No",
            })
        st.table(rows)
