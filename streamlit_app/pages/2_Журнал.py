"""Добавление материалов и список прочитанного"""

from __future__ import annotations

import streamlit as st

from src.components.cards import reading_item_card
from src.services import api_client as api

st.set_page_config(page_title="Журнал — SpacedReader", layout="centered")
st.title("Журнал")

SOURCE_KINDS: dict[str, str] = {
    "Статья": "article",
    "Книга": "book",
    "Научная работа": "paper",
    "Подкаст": "podcast",
    "Другое": "other",
}

with st.form("log_form", clear_on_submit=True):
    st.subheader("Добавить материал")

    title = st.text_input("Название", placeholder="Например: «Thinking, Fast and Slow»")
    source_label = st.selectbox("Тип", list(SOURCE_KINDS.keys()))
    source_url = st.text_input("Ссылка", placeholder="https://... (необязательно)")
    takeaway = st.text_area(
        "Главная мысль",
        placeholder="Что вы вынесли из этого материала? (20–500 символов)",
        height=120,
    )
    tags_raw = st.text_input("Теги", placeholder="психология, когнитивистика, наука (через запятую)")

    submitted = st.form_submit_button("Добавить", use_container_width=True)

if submitted:
    if not title.strip() or not takeaway.strip():
        st.warning("Заполните название и главную мысль.")
    else:
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        try:
            result = api.log_reading_item(
                title=title.strip(),
                source_kind=SOURCE_KINDS[source_label],
                source_url=source_url.strip() or None,
                takeaway=takeaway.strip(),
                tags=tags,
            )
            st.success(f"Добавлено: **{result['title']}**")
        except Exception as e:
            detail = getattr(e, "response", None)
            msg = detail.json().get("detail", {}).get("description", str(e)) if detail else str(e)
            st.error(f"Ошибка: {msg}")

st.markdown("---")
st.subheader("Прочитанное")

tag_filter = st.text_input("Фильтр по тегу", placeholder="Введите тег...")

try:
    data = api.list_reading_items(tag=tag_filter.strip() or None, limit=20)
    items = data["items"]
except Exception as e:
    st.error(f"Не удалось загрузить список: {e}")
    items = []

if not items:
    st.caption("Список пуст — добавьте первый материал выше.")
else:
    for item in items:
        reading_item_card(item)
