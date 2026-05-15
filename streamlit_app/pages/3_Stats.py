"""Статистика удержания и активности чтения"""

from __future__ import annotations

import streamlit as st

import streamlit_app.api_client as api

st.set_page_config(page_title="Статистика — SpacedReader", layout="centered")
st.title("Статистика")

col1, col2 = st.columns(2)

# --- удержание ---
try:
    ret = api.get_retention_stats()
    col1.metric("Удержание", f"{ret['overall_retention'] * 100:.1f}%")
    col2.metric("Средний EF", f"{ret['avg_ease_factor']:.2f}")
    col1.metric("Всего повторений", ret["total_reviews"])
except Exception as e:
    st.error(f"Ошибка загрузки статистики повторений: {e}")

st.divider()

# --- активность чтения ---
try:
    reading = api.get_reading_stats()
    st.metric("Всего элементов", reading["total_items"])

    by_week = reading["by_week"]
    if by_week:
        import pandas as pd

        df = pd.DataFrame(by_week)
        df["week"] = pd.to_datetime(df["week"])
        df = df.set_index("week").sort_index()
        st.subheader("Добавлений по неделям")
        st.bar_chart(df["count"])
    else:
        st.caption("Недостаточно данных для графика по неделям")

    by_tag = reading["by_tag"]
    if by_tag:
        import pandas as pd

        st.subheader("По тегам")
        df_tags = pd.DataFrame(by_tag).set_index("tag")
        st.bar_chart(df_tags["count"])
    else:
        st.caption("Тегов пока нет")

except Exception as e:
    st.error(f"Ошибка загрузки статистики чтения: {e}")
