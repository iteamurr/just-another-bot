"""Карточки на повторение сегодня"""

from __future__ import annotations

import streamlit as st

import api_client as api

st.set_page_config(page_title="Сегодня — SpacedReader", layout="centered")
st.title("Сегодня")

try:
    due = api.get_due_reviews()
except Exception as e:
    st.error(f"Не удалось загрузить карточки: {e}")
    st.stop()

cards = due["cards"]
total = due["total_due"]

if not cards:
    st.success("Все повторения на сегодня выполнены 🎉")
    st.stop()

st.caption(f"Осталось карточек: **{total}**")

# показываем первую карточку очереди
card = cards[0]
card_id = card["id"]

st.subheader("Вопрос")

# генерируем или показываем кешированный вопрос
if "question" not in st.session_state or st.session_state.get("card_id") != card_id:
    with st.spinner("Генерирую вопрос..."):
        try:
            q = api.generate_question(card_id)
            st.session_state["question"] = q["question"]
            st.session_state["card_id"] = card_id
        except Exception as e:
            st.error(f"Ошибка генерации вопроса: {e}")
            st.stop()

st.info(st.session_state["question"])

answer = st.text_area("Ваш ответ", key="answer_input")

st.subheader("Самооценка")
cols = st.columns(6)
grades = [
    (0, "0 — Провал"),
    (1, "1 — Почти"),
    (2, "2 — Плохо"),
    (3, "3 — Ок"),
    (4, "4 — Хорошо"),
    (5, "5 — Отлично"),
]

for col, (grade_val, label) in zip(cols, grades, strict=False):
    if col.button(str(grade_val), help=label, use_container_width=True):
        try:
            api.submit_grade(card_id, grade_val)
            # сбрасываем кеш вопроса — следующая карточка сгенерирует новый
            for key in ("question", "card_id", "answer_input"):
                st.session_state.pop(key, None)
            st.rerun()
        except Exception as e:
            st.error(f"Ошибка при сохранении оценки: {e}")
