import streamlit as st
from datetime import datetime
import json
import os
import pandas as pd

DATA_FILE = "timetable.json"

# ---------------- FILE FUNCTIONS ----------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- LOGIC FUNCTIONS ----------------
def get_current_and_next(day_data):
    now = datetime.now().strftime("%H:%M")
    current = "No class now"
    next_class = "No more classes today"

    for i, cls in enumerate(day_data):
        if cls["start"] <= now <= cls["end"]:
            if cls["subject"].lower() in ["break", "lunch"]:
                current = "🛑 Break Time"
            else:
                current = f"📘 {cls['subject']}"
            if i + 1 < len(day_data):
                next_class = day_data[i + 1]["subject"]
            break

        if cls["start"] > now and next_class == "No more classes today":
            next_class = cls["subject"]

    return current, next_class

# ---------------- UI ----------------
st.set_page_config("Timetable App", layout="centered")
st.title("📚 College Timetable App")

data = load_data()

menu = st.sidebar.selectbox(
    "Menu",
    ["Home", "Add / Edit Timetable", "Full Week Timetable"]
)

# ---------------- HOME ----------------
if menu == "Home":
    today = datetime.now().strftime("%A").lower()

    if today not in data:
        st.warning("No timetable found for today.")
    else:
        st.success(f"📅 Today: {today.capitalize()}")
        current, next_cls = get_current_and_next(data[today])
        st.info(f"🕒 Current: **{current}**")
        st.info(f"➡️ Next: **{next_cls}**")

# ---------------- ADD / EDIT ----------------
elif menu == "Add / Edit Timetable":
    st.subheader("➕ Add / Edit Timetable")

    day = st.selectbox(
        "Select Day",
        ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    )

    count = st.number_input(
        "Number of periods (including breaks)",
        min_value=1,
        max_value=12,
        step=1
    )

    day_data = []

    for i in range(count):
        st.markdown(f"### Period {i+1}")
        start = st.text_input("Start Time (HH:MM)", key=f"s{i}")
        end = st.text_input("End Time (HH:MM)", key=f"e{i}")
        subject = st.text_input(
            "Subject (Use 'Break' for breaks)",
            key=f"sub{i}"
        )

        if start and end and subject:
            day_data.append({
                "start": start,
                "end": end,
                "subject": subject
            })

    if st.button("💾 Save Timetable"):
        data[day] = day_data
        save_data(data)
        st.success("✅ Timetable saved successfully!")

# ---------------- FULL WEEK VIEW ----------------
elif menu == "Full Week Timetable":
    st.subheader("📅 Full Week Timetable")

    if not data:
        st.warning("No timetable data available.")
    else:
        for day, periods in data.items():
            st.markdown(f"## {day.capitalize()}")

            table = []
            for p in periods:
                table.append({
                    "Start": p["start"],
                    "End": p["end"],
                    "Subject": p["subject"]
                })

            df = pd.DataFrame(table)
            st.table(df)