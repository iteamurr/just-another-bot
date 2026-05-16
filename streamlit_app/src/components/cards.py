from __future__ import annotations

from typing import Any

import streamlit as st

_SOURCE_LABELS: dict[str, str] = {
    "article": "Статья",
    "book": "Книга",
    "paper": "Научная работа",
    "podcast": "Подкаст",
    "other": "Другое",
}


def reading_item_card(item: dict[str, Any]) -> None:
    kind = _SOURCE_LABELS.get(item["source"]["kind"], item["source"]["kind"])
    with st.expander(f"{item['title']} — {kind}"):
        st.write(item["takeaway"])
        if item["tags"]:
            st.caption("Теги: " + ", ".join(item["tags"]))
        if item["source"].get("url"):
            st.caption(f"[Источник]({item['source']['url']})")
