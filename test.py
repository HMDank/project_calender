import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "Week": ['1', '2', '3', '4'],
        "busy": [False, False, False, False],
        'progress':[1,2,3,4]
    }
)

st.data_editor(
    data_df,
    column_config={
        "busy": st.column_config.CheckboxColumn(
            "Busy?",
            default=False,
        ),
        "progress": st.column_config.ProgressColumn(
            "Progress",
            format="%f",
            min_value=0,
            max_value=10,
        ),
    },
    disabled=["widgets"],
    hide_index=True,
)
