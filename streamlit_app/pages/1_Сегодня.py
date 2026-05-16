"""Карточки на повторение"""

from __future__ import annotations

import streamlit as st

from src.services import api_client as api

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
    st.success("Все повторения на сегодня выполнены")
    st.caption("Возвращайтесь завтра или добавьте новые материалы в Журнале.")
    st.stop()

st.caption(f"Осталось: **{total}**")
st.markdown("---")

card = cards[0]
card_id = card["id"]

if "question" not in st.session_state or st.session_state.get("card_id") != card_id:
    with st.spinner("Формулирую вопрос..."):
        try:
            q = api.generate_question(card_id)
            st.session_state["question"] = q["question"]
            st.session_state["card_id"] = card_id
        except Exception as e:
            st.error(f"Не удалось сгенерировать вопрос: {e}")
            st.stop()

st.subheader("Вопрос")
st.info(st.session_state["question"])

st.text_area("Ваш ответ", key="answer_input", placeholder="Напишите ответ своими словами...")

st.markdown("---")
st.subheader("Как хорошо вы вспомнили?")

GRADES = [
    (0, "0", "Не помню совсем"),
    (1, "1", "Почти не помню"),
    (2, "2", "Вспомнил с трудом"),
    (3, "3", "Вспомнил с усилием"),
    (4, "4", "Вспомнил хорошо"),
    (5, "5", "Вспомнил без усилий"),
]

cols = st.columns(6)
for col, (grade_val, label, hint) in zip(cols, GRADES, strict=False):
    if col.button(label, help=hint, use_container_width=True):
        try:
            api.submit_grade(card_id, grade_val)
            for key in ("question", "card_id", "answer_input"):
                st.session_state.pop(key, None)
            st.rerun()
        except Exception as e:
            st.error(f"Не удалось сохранить оценку: {e}")
