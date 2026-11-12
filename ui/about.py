from __future__ import annotations

import streamlit as st


def render_about() -> None:
    st.header("About Rally")
    st.write(
        "Rally helps Zenith students find teammates for events teachers post."
    )

    st.subheader("How matching works")
    st.markdown(
        """
1. **Pair scoring.** Each pair gets a score from two parts:
   - **Skill complementarity (60%):** pairs with different skills score higher than pairs with the same skills.
   - **Availability overlap (40%):** pairs whose availability styles share time slots score higher.
2. **Greedy grouping.** Rally takes the next student in ID order, then repeatedly adds the student with the best average score against the current team, until the team reaches the event's team size.
3. **Suggestions.** You see your top 5 teammates by score, with each profile's `last_updated`.
"""
    )

    st.subheader("Known limitations")
    st.markdown(
        """
- Matching uses skills and availability style only. Languages and event notes are shown but not scored.
- Availability is one of three styles, not a real schedule.
- Grouping is greedy and order-dependent: early students get better fits, and the last team may be smaller than the event's team size.
- There is no real login. Teachers unlock with a shared PIN.
"""
    )