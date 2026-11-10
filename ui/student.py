from __future__ import annotations

import streamlit as st

import db

NEW_PROFILE: int = -1


def select_student() -> int:
    """Sidebar identity picker. Returns a student id, or NEW_PROFILE."""
    students = db.list_students()
    labels: dict[int, str] = {s.id: f"{s.name} ({s.batch})" for s in students}
    labels[NEW_PROFILE] = "➕ New profile"
    return st.sidebar.selectbox(
        "Who are you?",
        [NEW_PROFILE, *labels.keys() - {NEW_PROFILE}],
        format_func=lambda sid: labels[sid],
        key="student_id",
    )


def render_profile(student_id: int) -> None:
    st.header("My Profile")
    st.write(f"Selected id: {student_id}")  # temporary, replaced in 3c


def render_events(student_id: int) -> None:
    st.header("Browse Events")
    st.write(f"Selected id: {student_id}")  # temporary