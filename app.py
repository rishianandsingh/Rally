from __future__ import annotations

import streamlit as st

from ui import student, teacher

st.set_page_config(page_title="Rally", page_icon="🤝", layout="wide")


def main() -> None:
    st.sidebar.title("Rally")
    role = st.sidebar.radio("I am a", ["Student", "Teacher"])

    if role == "Student":
        student_id = student.select_student()
        page = st.sidebar.radio("Page", ["My Profile", "Browse Events"])
        if page == "My Profile":
            student.render_profile(student_id)
        else:
            student.render_events(student_id)
    else:
        teacher.render_teacher()


if __name__ == "__main__":
    main()
