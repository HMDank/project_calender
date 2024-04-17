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

st.header('Group Progress', anchor=False)
with open('tasks.yaml') as file:
    ongoing_tasks = yaml.load(file, Loader=SafeLoader)
tasks = []
progress = []
deadlines = []
participants = []
for entry in ongoing_tasks:
    tasks.append(entry['task'])
    progress.append(entry['progress'])
    deadlines.append(datetime.strptime(str(entry['deadline']), '%Y-%m-%d'))
    participants.append(entry['participants'])

df = pd.DataFrame(
    {
        "task": tasks,
        "progress": progress,
        "deadline": deadlines,
        "participants": participants
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
            format="D MMM YYYY",
        ),
    },
    use_container_width=True,
    hide_index=True,
)

st.header('Group Schedule', anchor=False)


plot = create_calender_plot()
st.plotly_chart(plot, use_container_width=True)
