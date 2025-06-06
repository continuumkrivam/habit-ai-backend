import streamlit as st
import datetime
import pandas as pd

st.set_page_config(page_title="Habit League", layout="wide")
st.title("🧠 Habit League Tracker")

# Step 1: User Info
with st.form("user_info"):
    name = st.text_input("Name", help="Required")
    age = st.number_input("Age", min_value=10, max_value=100)
    gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
    location = st.text_input("Location")
    submit_user = st.form_submit_button("Find Goals")

if submit_user:
    if not name.strip():
        st.warning("Please enter your name to continue.")
    else:
        goals = [
            "1. Improve daily focus with 1 hour of deep work",
            "2. Build strength through consistent workouts",
            "3. Enhance well-being with nightly journaling"
        ]
        st.session_state["goals"] = goals
        st.session_state["user_name"] = name.strip().split()[0]  # First name
        st.success(f"Goals loaded for {st.session_state['user_name']}!")

# Step 2: Show goals, start date, duration
if "goals" in st.session_state:
    selected_goal = st.selectbox("Select a goal to focus on", st.session_state["goals"])
    start_date = st.date_input("Select Habit League Start Date", min_value=datetime.date.today())
    duration_days = st.slider("League Duration (days)", 7, 60, 21)
    frequency_all = st.selectbox("Select Habit Frequency", ["Daily", "Weekly"])

    if st.button("Generate Habits"):
        st.session_state.update({
            "selected_goal": selected_goal,
            "start_date": start_date,
            "duration_days": duration_days,
            "frequency_all": frequency_all,
            "generate_habits_clicked": True
        })

# Step 3: Mock Habits
if st.session_state.get("generate_habits_clicked", False):
    with st.spinner("Loading habits..."):
        habits = [
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
        st.session_state["habits"] = habits
        st.session_state["generate_habits_clicked"] = False
        st.success("Habits ready!")

# Step 4: Rate habits
if "habits" in st.session_state:
    st.subheader("📝 Rate difficulty (1–5)")
    habit_data = []
    for i, habit in enumerate(st.session_state["habits"]):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(habit)
        with col2:
            difficulty = st.slider(f"Difficulty {i+1}", 1, 5, key=f"diff_{i}")
        habit_data.append({
            "habit": habit,
            "difficulty": difficulty,
            "frequency": st.session_state["frequency_all"]
        })

    if st.button("Start League"):
        sorted_habits = sorted(habit_data, key=lambda x: x["difficulty"])[:6]
        st.session_state["selected_habits"] = sorted_habits

        start = st.session_state["start_date"]
        duration = st.session_state["duration_days"]
        days = [start + datetime.timedelta(days=i) for i in range(duration)]

        progress_df = pd.DataFrame(
            [[False]*6 for _ in days],
            columns=[d.strftime("%Y-%m-%d") for d in days],
            index=[h["habit"] for h in sorted_habits]
        )
        st.session_state["progress_df"] = progress_df
        st.success(f"{st.session_state['user_name']}, your league has started!")

# Step 5: Calendar + Streak Tracker
if "progress_df" in st.session_state:
    st.subheader("📆 Your Habit Calendar")

    df = st.session_state["progress_df"]

    with st.container():
        st.markdown("### ✅ Track Habits")
        edited_df = df.copy()

        for i, habit in enumerate(df.index):
            row = []
            cols = st.columns(len(df.columns) + 1)
            cols[0].markdown(f"**{habit}**")
            for j, day in enumerate(df.columns):
                key = f"{habit}_{day}"
                checkbox = cols[j+1].checkbox("", value=df.loc[habit, day], key=key)
                edited_df.loc[habit, day] = checkbox

        st.session_state["progress_df"] = edited_df

        # 🔥 Streaks per habit
        st.markdown("### 🔥 Longest Streaks (per habit)")
        for habit in df.index:
            streak = 0
            max_streak = 0
            for status in df.loc[habit]:
                if status:
                    streak += 1
                    max_streak = max(max_streak, streak)
                else:
                    streak = 0
            st.markdown(f"**{habit}** → 🔥 {max_streak} days")

        # 🌟 Special streak for 4+ habit days
        st.markdown("### 🌟 Days with 4 or More Habits Completed")
        streak = 0
        max_streak = 0
        for col in df.columns:
            completed = df[col].sum()
            if completed >= 4:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0
        st.markdown(f"🏆 Max League Day Streak (4+ habits): **{max_streak} days**")

        # 💾 Download Progress
        st.download_button(
            label="💾 Download Progress",
            data=edited_df.to_csv().encode("utf-8"),
            file_name="habit_progress.csv",
            mime="text/csv"
        )
