import streamlit as st
import pandas as pd
import io
import re

# The raw data from the provided timetable
RAW_DATA = """NAIROBI CITY CAMPUS JANUARY TO APRIL 2025 DRAFT TEACHING TIMETABLE
ARTISAN CEE TERM 2
,0800-1100,1100-1400,1400-1700
Monday,,,LECT Y MATHEMATICS EEE 624 Mathematics I ST902
Tuesday,TABITHA WANJIKU EEE 622 General Studies ST903,,
Wednesday,ABIGAIL JERUTO EEE 623 General Science ST903,"ABIGAIL JERUTO\nEEE 620 Electrical Installation Trade\nTheory\nST103",
Thursday,,JOSEPH MACHARIA EEE 602 Trade Practice ST103,JOSEPH MACHARIA EEE 602 Trade Practice ST103
Friday,GIBSON KIPKOECH EEE 621 Applied Geometry ST103,,
ARTISAN CEE TERM 3
,0800-1100,1100-1400,1400-1700
Monday,TABITHA WANJIKU EEE 622 General Studies ST903,,
Tuesday,ABIGAIL JERUTO EEE 623 General Science ST903,"ABIGAIL JERUTO\nEEE 620 Electrical Installation Trade\nTheory\nST103",
Wednesday,,JOSEPH MACHARIA EEE 602 Trade Practice ST103,JOSEPH MACHARIA EEE 602 Trade Practice ST103
Thursday,GIBSON KIPKOECH EEE 621 Applied Geometry ST103,,
Friday,,,LECT Y MATHEMATICS EEE 624 Mathematics I ST902
DIPLOMA Y2S1
,0800-1100,1100-1400,1400-1700
Monday,,,LECT Y MATHEMATICS EEE 624 Mathematics I ST902
Tuesday,TABITHA WANJIKU EEE 622 General Studies ST903,,
Wednesday,ABIGAIL JERUTO EEE 623 General Science ST903,"ABIGAIL JERUTO\nEEE 620 Electrical Installation Trade\nTheory\nST103",
Thursday,,JOSEPH MACHARIA EEE 602 Trade Practice ST103,JOSEPH MACHARIA EEE 602 Trade Practice ST103
Friday,GIBSON KIPKOECH EEE 621 Applied Geometry ST103,,
"""

@st.cache_data
def load_and_structure_data():
    """Parses the raw timetable data into a structured DataFrame."""
    structured_data = []
    current_program = ""
    current_times = []
    lines = RAW_DATA.split('\n')

    for i, line in enumerate(lines):
        if "DRAFT TEACHING TIMETABLE" in line:
            continue
        if "TERM" in line or "DIPLOMA" in line:
            current_program = line.strip()
        elif "0800-1100" in line:
            current_times = line.strip().split(',')
            if current_times[0] == '':
                current_times.pop(0)
        elif len(line.split(',')) > 1:
            parts = line.split(',', 1)
            day = parts[0].strip()
            if not day:
                continue
            entries = parts[1].split(',')
            for j, entry in enumerate(entries):
                entry = entry.strip().replace('"', '')
                if entry:
                    match = re.search(r'([A-Z\s]+)\s(EEE\s\d+\s.*)', entry)
                    if match:
                        lecturer = match.group(1).strip()
                        course_info = match.group(2).strip()
                    else:
                        lecturer = "Not specified"
                        course_info = entry

                    course_parts = course_info.split(' ', 2)
                    course_code = course_parts[0] + " " + course_parts[1]
                    course_name = course_parts[2] if len(course_parts) > 2 else ""

                    structured_data.append({
                        'Program': current_program,
                        'Day': day,
                        'Time': current_times[j],
                        'Lecturer': lecturer,
                        'Course Code': course_code,
                        'Course Name': course_name
                    })

    return pd.DataFrame(structured_data)

# --- Streamlit App Interface ---
st.title("Draft Teaching Timetable Analysis 🗓️")
st.write("This app displays and analyzes the structured teaching timetable data.")

df = load_and_structure_data()

if not df.empty:
    st.subheader("1. Full Timetable")
    st.dataframe(df)

    st.subheader("2. Analysis")

    # Analysis 1: Classes per Lecturer
    st.markdown("**Classes per Lecturer**")
    lecturer_counts = df['Lecturer'].value_counts().reset_index()
    lecturer_counts.columns = ['Lecturer', 'Number of Classes']
    st.bar_chart(lecturer_counts.set_index('Lecturer'))
    st.write("This chart shows how many classes each lecturer is teaching.")

    # Analysis 2: Classes per Day
    st.markdown("**Classes per Day**")
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    day_counts = df['Day'].value_counts().reindex(day_order).fillna(0)
    st.bar_chart(day_counts)
    st.write("This chart shows the total number of classes scheduled for each day of the week.")
