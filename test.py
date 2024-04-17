import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "Week": ['1', '2', '3', '4'],
        "busy": [False, False, False, False],
    }
)

st.data_editor(
    data_df,
    column_config={
        "busy": st.column_config.CheckboxColumn(
            "Busy?",
            default=False,
        )
    },
    disabled=["widgets"],
    hide_index=True,
)
