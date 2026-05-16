"""Статистика удержания и активности"""

from __future__ import annotations

import streamlit as st

from src.components.charts import tag_chart, weekly_chart
from src.services import api_client as api

st.set_page_config(page_title="Статистика — SpacedReader", layout="centered")
st.title("Статистика")

# --- повторения ---
try:
    ret = api.get_retention_stats()

    st.subheader("Повторения")
    c1, c2, c3 = st.columns(3)
    c1.metric("Удержание", f"{ret['overall_retention'] * 100:.1f}%")
    c2.metric("Средний EF", f"{ret['avg_ease_factor']:.2f}")
    c3.metric("Всего сессий", ret["total_reviews"])
except Exception as e:
    st.error(f"Не удалось загрузить статистику повторений: {e}")

st.markdown("---")

# --- чтение ---
try:
    reading = api.get_reading_stats()

    st.subheader("Чтение")
    st.metric("Всего материалов", reading["total_items"])

    if reading["by_week"]:
        st.caption("Добавлено по неделям")
        weekly_chart(reading["by_week"])
    else:
        st.caption("Недостаточно данных для графика по неделям.")

    if reading["by_tag"]:
        st.caption("Распределение по тегам")
        tag_chart(reading["by_tag"])
    else:
        st.caption("Теги ещё не добавлены.")

except Exception as e:
    st.error(f"Не удалось загрузить статистику чтения: {e}")
