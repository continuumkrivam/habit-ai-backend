import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Habit League Tracker", layout="wide")
st.title("🧠 Habit League Tracker")

# Step 1: User Info
if "user_info" not in st.session_state:
    with st.form("user_info"):
        name = st.text_input("Name")
        if not name:
            st.warning("Name is required to proceed.")
        age = st.number_input("Age", min_value=10, max_value=100)
        gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Other"])
        location = st.text_input("Location")
        start_date = st.date_input("Start Date", min_value=datetime.date.today())
        league_duration = st.selectbox("How long is your habit league?", ["7 days", "14 days", "21 days", "30 days"])
        submit_user = st.form_submit_button("Find Goals")

        if submit_user and name:
            st.session_state["user_info"] = {
                "name": name,
                "first_name": name.strip().split()[0],
                "age": age,
                "gender": gender,
                "location": location,
                "start_date": start_date,
                "duration": int(league_duration.split()[0])
            }
            st.session_state["goals"] = [
                "Improve focus",
                "Build morning routine",
                "Reduce screen time",
                "Boost physical fitness"
            ]
            st.experimental_rerun()  # <--- force a safe rerun
else:
    st.success(f"Nice, {st.session_state['user_info']['first_name']}! Here are your AI-suggested goals.")

# Step 2: Select Goal
if "goals" in st.session_state:
    selected_goal = st.selectbox("🎯 Select a goal to focus on", st.session_state["goals"])
    if st.button("Generate Habits"):
        st.session_state["habits"] = [
            "Read 10 pages of a book",
            "Journal for 5 minutes",
            "Walk for 20 minutes",
            "Plan next day in advance",
            "Do 15 push-ups",
            "Meditate for 10 minutes",
            "Stretch in the morning",
            "No screen after 9 PM",
            "Drink 2L water",
            "Eat 1 healthy meal"
        ]
        st.success("Habits generated based on your goal!")

# Step 3: Rate and Select Frequency
if "habits" in st.session_state:
    st.subheader("📝 Rate difficulty (1–5) and select frequency")
    habit_data = []
    for i, habit in enumerate(st.session_state["habits"]):
        col1, col2, col3 = st.columns([3, 1, 2])
        with col1:
            st.markdown(habit)
        with col2:
            difficulty = st.slider(f"Difficulty {i+1}", 1, 5, key=f"diff_{i}")
        with col3:
            freq = st.selectbox("Frequency", ["Daily", "Weekly"], key=f"freq_{i}")
        habit_data.append({"habit": habit, "difficulty": difficulty, "frequency": freq})

    if st.button("Start League"):
        st.session_state["selected_habits"] = habit_data
        st.success("League started! Here's your tracker ⬇️")

# Step 4: Calendar Tracker
if "selected_habits" in st.session_state:
    st.subheader("📅 Habit Calendar")
    user_info = st.session_state["user_info"]
    habits = st.session_state["selected_habits"]
    sorted_habits = sorted(habits, key=lambda x: x["difficulty"])
    start = user_info["start_date"]
    duration = user_info["duration"]
    days = [start + datetime.timedelta(days=i) for i in range(duration)]

    progress_df = pd.DataFrame(
        [[False]*len(days) for _ in sorted_habits],
        columns=[d.strftime("%Y-%m-%d") for d in days],
        index=[h["habit"] for h in sorted_habits]
    )

    edited_df = st.data_editor(
        progress_df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=False,
        column_config={col: st.column_config.CheckboxColumn() for col in progress_df.columns}
    )

    # Step 5: Streak Calculation
    st.subheader("🔥 Streak Tracker")
    streaks = {habit: 0 for habit in edited_df.index}
    current_streaks = {habit: 0 for habit in edited_df.index}
    special_days = 0

    for col in edited_df.columns:
        checked_today = 0
        for habit in edited_df.index:
            if edited_df.loc[habit, col]:
                current_streaks[habit] += 1
                streaks[habit] = max(streaks[habit], current_streaks[habit])
                checked_today += 1
            else:
                current_streaks[habit] = 0
        if checked_today >= 4:
            special_days += 1

    for habit, streak in streaks.items():
        st.write(f"🏁 **{habit}**: Longest Streak = {streak} days")

    st.markdown(f"✅ **Special Streak Days (4+ habits done)**: {special_days} out of {duration}")
