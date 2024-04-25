import streamlit as st
import pandas as pd
from plot import create_calender_plot, create_dataframe
from st_pages import show_pages_from_config, hide_pages
from datetime import datetime, date
import pymongo
import yaml
from yaml.loader import SafeLoader
from database import retrieve_user_data, update_user
st.set_page_config(layout="wide",
                   page_title='Calendar',)
hide_pages(["Back"])
show_pages_from_config()

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

users_data = retrieve_user_data([user_info["name"] for user_info in config['credentials']['usernames'].values()])
# st.write(users_data)
with st.sidebar:
    st.subheader('Group Status', anchor=False)
    for user_data in users_data:
        if user_data[0]['status'] == 'Free':
            st.metric('d', f"{user_data[0]['name'].capitalize()}", label_visibility="collapsed", delta=f"{user_data[0]['status']}", delta_color='off')
        elif user_data[0]['status'] == 'Active':
            st.metric('d', f"{user_data[0]['name'].capitalize()}", label_visibility="collapsed", delta=f"{user_data[0]['status']}", delta_color='normal')
        else:
            st.metric('d', f"{user_data[0]['name'].capitalize()}", label_visibility="collapsed", delta=f"{user_data[0]['status']}", delta_color='inverse')

st.header('Ongoing Tasks', anchor=False)
with open('tasks.yaml') as file:
    ongoing_tasks = yaml.load(file, Loader=SafeLoader)
tasks = []
progress = []
deadlines = []
participants = []
if ongoing_tasks:
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
        "participants": participants,
        'completed': [False for _ in range(len(tasks))],
    }
)
if df is not None:
    data = st.data_editor(
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

            "deadline": st.column_config.Column(
                "Deadline",
            ),
            'completed': st.column_config.Column(
                'Completed',
            )
        },
        use_container_width=True,
        hide_index=True,
    )

new_data = data[data['completed'] == False]
if new_data is not None:
    updated_tasks = []
    for index, row in new_data.iterrows():
        task_dict = {
            "task": row['task'],
            "progress": row['progress'],
            "deadline": row['deadline'].strftime('%Y-%m-%d'),  # Convert datetime back to string format
            "participants": row['participants'],
            "completed": row['completed']
        }
        updated_tasks.append(task_dict)
with open('tasks.yaml', 'w') as task_file:
    yaml.dump(updated_tasks, task_file, default_flow_style=False)


st.header('Group Schedule', anchor=False)
st.dataframe(create_dataframe(users_data))