import streamlit as st
import pandas as pd
from plot import create_calender_plot, create_dataframe, datetime_to_str
from st_pages import show_pages_from_config, hide_pages
from datetime import datetime, date, timedelta
import pymongo
import yaml
from yaml.loader import SafeLoader
from database import retrieve_user_data, update_user, retrieve_tasks, remove_task
st.set_page_config(layout="wide",
                   page_title='Calendar',)
hide_pages(["Back"])
show_pages_from_config()


def mask_df(df, date_range):
    df.columns = pd.to_datetime(df.columns)
    start_date = date_range[0]
    end_date = date_range[1] if len(date_range) > 1 else date_range[0] + timedelta(days=10)
    mask = (df.columns >= pd.Timestamp(start_date)) & (df.columns <= pd.Timestamp(end_date))
    masked_df = df.loc[:, mask]
    masked_df.columns = [col.date() for col in masked_df.columns]

    def color_background(val):
        if val == 'Busy':
            return f'background-color: #e38686; font-weight: bold;'
        if val == "Active":
            return f'background-color: #9ee096; font-weight: bold;'

    styled_df = masked_df.style.map(color_background)
    return styled_df


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
ongoing_tasks = retrieve_tasks()
names = []
progress = []
deadlines = []
participants = []
if ongoing_tasks:
    for task in ongoing_tasks:
        if task:
            names.append(task[0]['name'])
            progress.append(task[0]['progress'])
            deadlines.append(datetime.strptime(str(task[0]['deadline']), '%Y-%m-%d'))
            participants.append(task[0]['participants'])

df = pd.DataFrame(
    {
        "name": names,
        "progress": progress,
        "deadline": deadlines,
        "participants": participants,
        'completed': [False for _ in range(len(names))],
    }
)
if df is not None:
    data = st.data_editor(
        df,
        column_config={
            "name": "Name",
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

deleted_data = data[data['completed'] == True]
if deleted_data is not None:
    remove_task(deleted_data['name'].tolist())

st.header('Group Schedule', anchor=False)
column1, column2, column3 = st.columns(3)
with column1:
    date_range = st.date_input('Pick a range', (date.today(), date.today() + timedelta(days=10)), min_value=date.today(), max_value=date(2024, 12, 31), label_visibility='collapsed')
schedule_df = create_dataframe(users_data)
st.dataframe(mask_df(schedule_df, date_range))
