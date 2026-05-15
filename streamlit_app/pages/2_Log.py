"""Добавление нового элемента и список недавних"""
from __future__ import annotations

import streamlit as st

import streamlit_app.api_client as api

st.set_page_config(page_title="Журнал — SpacedReader", layout="centered")
st.title("Журнал")

SOURCE_KINDS = ["article", "book", "paper", "podcast", "other"]

with st.form("log_form", clear_on_submit=True):
    title = st.text_input("Название *")
    source_kind = st.selectbox("Тип источника", SOURCE_KINDS)
    source_url = st.text_input("URL (необязательно)")
    takeaway = st.text_area("Заметка (20–500 символов) *")
    tags_raw = st.text_input("Теги через запятую")
    submitted = st.form_submit_button("Добавить")

if submitted:
    if not title or not takeaway:
        st.warning("Заполните название и заметку")
    else:
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        try:
            result = api.log_reading_item(
                title=title,
                source_kind=source_kind,
                source_url=source_url or None,
                takeaway=takeaway,
                tags=tags,
            )
            st.success(f"Добавлено: **{result['title']}**")
        except Exception as e:
            detail = getattr(e, "response", None)
            if detail is not None:
                msg = detail.json().get("detail", {}).get("description", str(e))
            else:
                msg = str(e)
            st.error(f"Ошибка: {msg}")

st.divider()
st.subheader("Недавние")

tag_filter = st.text_input("Фильтр по тегу")

try:
    data = api.list_reading_items(tag=tag_filter or None, limit=20)
    items = data["items"]
except Exception as e:
    st.error(f"Не удалось загрузить список: {e}")
    items = []

if not items:
    st.caption("Пока ничего нет")
else:
    for item in items:
        with st.expander(f"📖 {item['title']} · {item['source']['kind']}"):
            st.write(item["takeaway"])
            if item["tags"]:
                st.caption("Теги: " + ", ".join(item["tags"]))
