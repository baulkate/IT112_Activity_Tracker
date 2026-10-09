import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Student Missing Activity Tracker", page_icon="📚", layout="centered"
)

st.title("📚 Single-Subject Activity & Grade Tracker")
st.markdown("Enter a **Student ID** below to look up their activities.")


# Load Data (Using mock data for demonstration)
@st.cache_data
def load_data():
  data = {
      "Student ID": ["S1042", "S1042", "S1042", "S1042", "S1043", "S1043"],
      "Student Name": [
          "Alex Smith",
          "Alex Smith",
          "Alex Smith",
          "Alex Smith",
          "Jane Doe",
          "Jane Doe",
      ],
      "Assignment Name": [
          "Solving Quadratic Equations",
          "Quiz 2: Factoring",
          "Graphing Parabolas Lab",
          "Chapter 2 Practice Test",
          "Solving Quadratic Equations",
          "Quiz 2: Factoring",
      ],
      "Status": [
          "Graded",
          "Missing",
          "In Progress",
          "Missing",
          "Graded",
          "Graded",
      ],
      "Points Possible": [25, 50, 40, 30, 25, 50],
      "Final Score": [22, 0, 0, 0, 25, 42],
  }
  return pd.DataFrame(data)


df = load_data()

# Search Input
search_id = st.text_input(
    "Enter Student ID:", placeholder="e.g., S1042"
).strip()

if search_id:
  # Filter data for the entered ID (case-insensitive)
  student_df = df[df["Student ID"].str.upper() == search_id.upper()]

  if not student_df.empty:
    student_name = student_df["Student Name"].iloc[0]

    st.success(f"Found records for: **{student_name}** ({search_id.upper()})")

    # Calculate Metrics
    missing_count = len(student_df[student_df["Status"] == "Missing"])
    graded_items = student_df[student_df["Status"] == "Graded"]
    total_possible = graded_items["Points Possible"].sum()
    total_earned = graded_items["Final Score"].sum()
    current_grade = (
        (total_earned / total_possible) * 100 if total_possible > 0 else 0
    )

    # Display Metrics in Columns
    col1, col2 = st.columns(2)
    col1.metric(label="Current Grade", value=f"{current_grade:.1f}%")
    col2.metric(
        label="Missing Assignments",
        value=missing_count,
        delta=-missing_count if missing_count > 0 else "None",
        delta_color="inverse",
    )

    # Display Activity Table
    st.markdown("### Activity Breakdown")
    st.dataframe(
        student_df[
            ["Assignment Name", "Status", "Points Possible", "Final Score"]
        ],
        use_container_width=True,
    )

  else:
    st.error(
        f"No records found for Student ID '{search_id}'. Please check and try"
        " again."
    )