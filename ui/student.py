from __future__ import annotations

import streamlit as st


def render_profile() -> None:
    st.header("My Profile")
    st.info("Profile form goes here.")


def render_events() -> None:
    st.header("Browse Events")
    st.info("Event list goes here.")