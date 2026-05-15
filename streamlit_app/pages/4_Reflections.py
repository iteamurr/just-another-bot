"""Еженедельные резюме"""

from __future__ import annotations

import streamlit as st

import streamlit_app.api_client as api

st.set_page_config(page_title="Рефлексии — SpacedReader", layout="centered")
st.title("Рефлексии")

st.write("Резюме по материалам, добавленным за последние 7 дней.")

if st.button("Сгенерировать резюме", type="primary"):
    with st.spinner("Генерирую..."):
        try:
            result = api.generate_weekly_summary()
            st.session_state["summary"] = result["summary"]
            st.session_state["items_count"] = result["items_count"]
        except Exception as e:
            st.error(f"Ошибка: {e}")

if "summary" in st.session_state:
    st.caption(f"Охвачено элементов: **{st.session_state['items_count']}**")
    st.markdown(st.session_state["summary"])
