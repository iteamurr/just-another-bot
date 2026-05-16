"""Еженедельное резюме"""

from __future__ import annotations

import streamlit as st

from src.services import api_client as api

st.set_page_config(page_title="Рефлексии — SpacedReader", layout="centered")
st.title("Рефлексии")
st.caption("Еженедельное резюме материалов, добавленных за последние 7 дней.")

st.markdown("---")

if st.button("Сгенерировать резюме", type="primary", use_container_width=True):
    with st.spinner("Анализирую прочитанное..."):
        try:
            result = api.generate_weekly_summary()
            st.session_state["summary"] = result["summary"]
            st.session_state["items_count"] = result["items_count"]
        except Exception as e:
            st.error(f"Не удалось сгенерировать резюме: {e}")

if "summary" in st.session_state:
    count = st.session_state["items_count"]
    if count == 0:
        st.info("За последние 7 дней материалы не добавлялись.")
    else:
        st.caption(f"Охвачено материалов: **{count}**")
        st.markdown("---")
        st.markdown(st.session_state["summary"])
