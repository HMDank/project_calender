import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from plot import create_calender_plot
from st_pages import show_pages_from_config, hide_pages
from datetime import datetime
import yaml
from yaml.loader import SafeLoader
st.set_page_config(layout="wide",
                   page_title='Calendar',)
hide_pages(["Back"])
show_pages_from_config()
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

with st.sidebar:
    st.subheader('Group Status', anchor=False)
    for username, info in config['credentials']['usernames'].items():
        if info['status'] == 'Free':
            st.metric('d', f"{info['name']}", label_visibility="collapsed", delta=f'{info["status"]}', delta_color='off')
        elif info['status'] == 'Active':
            st.metric('d', f"{info['name']}", label_visibility="collapsed", delta=f'{info["status"]}', delta_color='normal')
        else:
            st.metric('d', f"{info['name']}", label_visibility="collapsed", delta=f'{info["status"]}', delta_color='inverse')
st.header('Group Schedule', anchor=False)

df = pd.DataFrame(
    {
        "task": ["Power BI 1", "Task 2", "Task 3","Task 4"],
        "progress": [20, 55, 100, 8],
        "participants":[
            ["Thằng thứ 1", "Thằng thứ 2", "Thằng thứ 3", "Thằng thứ 4"],
            ["Thằng thứ 5", "Thằng thứ 6", "Thằng thứ 7", "Thằng thứ 8"],
            ["Thằng thứ 9", "Thằng thứ 10", "Thằng thứ 11", "Thằng thứ 12"],
            ["Thằng thứ 13", "Thằng thứ 14", "Thằng thứ 15", "Thằng thứ 16"],
        ],
        "deadline":[
            datetime(2024, 2, 5, 12, 30),
            datetime(2023, 11, 10, 18, 0),
            datetime(2024, 3, 11, 20, 10),
            datetime(2023, 9, 12, 3, 0),
        ]
    }
)
st.dataframe(
    df,
    column_config={
        "task": "Task",
        "progress": st.column_config.ProgressColumn(
            "Progress (%)",
            min_value=0,
            max_value=100,
        ),
        "participants": st.column_config.ListColumn(
            "Participants"
        ),

        "deadline": st.column_config.DatetimeColumn(
            "Deadline",
            min_value=datetime(2023, 6, 1),
            max_value=datetime(2025, 1, 1),
            format="D MMM YYYY, h:mm a",
            step=60,
        ),
    },
    use_container_width = True,
    hide_index=True,
)


st.header('Group Progress', anchor=False)

plot = create_calender_plot()
st.plotly_chart(plot, use_container_width=True)