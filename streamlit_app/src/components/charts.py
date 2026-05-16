from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st


def weekly_chart(data: list[dict[str, Any]]) -> None:
    df = pd.DataFrame(data)
    df["week"] = pd.to_datetime(df["week"])
    df = df.set_index("week").sort_index()
    st.bar_chart(df["count"])


def tag_chart(data: list[dict[str, Any]]) -> None:
    df = pd.DataFrame(data).set_index("tag")
    st.bar_chart(df["count"])
