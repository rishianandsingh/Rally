from __future__ import annotations

import hmac
from datetime import date

import streamlit as st

import db
from config import get_teacher_pin
from validation import EventInput, validate_event


def _is_authed() -> bool:
    return st.session_state.get("teacher_authed", False)


def render_teacher() -> None:
    st.header("Teacher: Create Event")

    if not _is_authed():
        pin = st.text_input("Teacher PIN", type="password")
        if st.button("Unlock"):
            try:
                expected = get_teacher_pin()
            except RuntimeError as e:
                st.error(str(e))
                return
            if hmac.compare_digest(pin.encode(), expected.encode()):
                st.session_state["teacher_authed"] = True
                st.rerun()
            else:
                st.error("Incorrect PIN.")
        return

    with st.form("create_event", clear_on_submit=True):
        title = st.text_input("Title")
        description = st.text_area("Description")
        team_size = st.number_input("Team size", min_value=2, max_value=10, value=3, step=1)
        event_date = st.date_input("Date", min_value=date.today())
        submitted = st.form_submit_button("Create event")

    if submitted:
        event = EventInput(title, description, int(team_size), event_date)
        if errors := validate_event(event):
            for msg in errors:
                st.error(msg)
        else:
            db.create_event(
                event.title, event.description, event.team_size, event.event_date.isoformat()
            )
            st.success(f"Created: {event.title}")