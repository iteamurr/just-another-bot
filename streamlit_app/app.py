"""Главная страница"""

from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="SpacedReader", page_icon="📚", layout="centered")

st.title("SpacedReader")
st.caption("Читай. Повторяй. Запоминай.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Сегодня**")
    st.caption("Карточки, которые пора повторить")

    st.markdown("**Статистика**")
    st.caption("Удержание, активность и теги")

with col2:
    st.markdown("**Журнал**")
    st.caption("Добавить статью, книгу или подкаст")

    st.markdown("**Рефлексии**")
    st.caption("Еженедельное резюме прочитанного")
