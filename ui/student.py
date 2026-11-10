from __future__ import annotations

import streamlit as st

import db
from options import AVAILABILITY_STYLES, BATCHES, LANGUAGES, SKILLS
from matcher import from_student, suggest_teammates

NEW_PROFILE: int = -1


def select_student() -> int:
    """Sidebar identity picker. Returns a student id, or NEW_PROFILE."""
    pending = st.session_state.pop("_pending_student_id", None)
    if pending is not None:
        st.session_state["student_id"] = pending

    students = db.list_students()
    labels: dict[int, str] = {NEW_PROFILE: "➕ New profile"}
    labels.update({s.id: f"{s.name} ({s.batch})" for s in students})
    return st.sidebar.selectbox(
        "Who are you?",
        list(labels),
        format_func=lambda sid: labels[sid],
        key="student_id",
    )


def render_profile(student_id: int) -> None:
    is_new = student_id == NEW_PROFILE
    existing = None if is_new else db.get_student(student_id)

    st.header("Create Profile" if is_new else "My Profile")
    if existing:
        st.caption(f"Last updated: {existing.last_updated[:10]}")

    k = f"p{student_id}_"  # per-student widget keys so prefill resets on switch
    with st.form(f"profile_form_{student_id}"):
        name = st.text_input("Name", value=existing.name if existing else "", key=k + "name")
        batch = st.selectbox(
            "Batch",
            BATCHES,
            index=BATCHES.index(existing.batch) if existing and existing.batch in BATCHES else 0,
            key=k + "batch",
        )
        skills = st.multiselect(
            "Skills",
            SKILLS,
            default=[s for s in existing.skills if s in SKILLS] if existing else [],
            key=k + "skills",
        )
        languages = st.multiselect(
            "Languages",
            LANGUAGES,
            default=[x for x in existing.languages if x in LANGUAGES] if existing else [],
            key=k + "langs",
        )
        availability = st.selectbox(
            "Availability",
            AVAILABILITY_STYLES,
            index=(
                AVAILABILITY_STYLES.index(existing.availability_style)
                if existing and existing.availability_style in AVAILABILITY_STYLES
                else 0
            ),
            key=k + "avail",
        )
        submitted = st.form_submit_button("Save profile")

    if not submitted:
        return
    if not name.strip():
        st.error("Name is required.")
        return
    if not skills:
        st.error("Pick at least one skill; matching depends on it.")
        return

    if is_new:
        new_id = db.add_student(name, batch, skills, languages, availability)
        st.session_state["_pending_student_id"] = new_id
        st.rerun()
    else:
        db.update_student(student_id, name, batch, skills, languages, availability)
        st.success("Profile saved.")


def render_events(student_id: int) -> None:
    st.header("Browse Events")
    if student_id == NEW_PROFILE:
        st.info("Create your profile first (My Profile page), then come back to join events.")
        return
    me = db.get_student(student_id)
    if me is None:
        st.error("Selected student not found.")
        return
    events = db.list_events()
    if not events:
        st.info("No events yet. A teacher needs to create one.")
        return
    for event in events:
        _render_event(event, me)


def _render_event(event: db.Event, me: db.Student) -> None:
    entries = db.get_entries(event.id)
    my_note = next((note for s, note in entries if s.id == me.id), None)
    joined = my_note is not None

    title = f"{event.title}  ·  {event.date}  ·  teams of {event.team_size}  ·  {len(entries)} joined"
    with st.expander(title):
        if event.description:
            st.write(event.description)

        if joined:
            st.success(f"You've joined. Your note: {my_note or '(none)'}")
        else:
            with st.form(f"join_{event.id}"):
                note = st.text_area(
                    "Short note for potential teammates",
                    key=f"note_{event.id}",
                )
                submitted = st.form_submit_button("Join this event")
            if submitted:
                try:
                    db.add_entry(me.id, event.id, note.strip())
                except ValueError as e:
                    st.error(str(e))
                else:
                    st.rerun()

        others = [(s, n) for s, n in entries if s.id != me.id]
        if not others:
            st.caption("No one else has joined yet.")
            return

        by_id = {s.id: (s, n) for s, n in others}
        ranked = suggest_teammates(
            from_student(me), [from_student(s) for s, _ in others], k=5
        )
        st.subheader("Suggested teammates")
        st.dataframe(
            [
                {
                    "Name": by_id[sid][0].name,
                    "Match": round(score, 2),
                    "Skills": ", ".join(by_id[sid][0].skills),
                    "Availability": by_id[sid][0].availability_style,
                    "Profile updated": by_id[sid][0].last_updated[:10],
                    "Note": by_id[sid][1],
                }
                for sid, score in ranked
            ],
            hide_index=True,
        )