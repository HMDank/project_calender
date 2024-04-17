import streamlit as st
import yaml
from datetime import datetime, timedelta
from yaml.loader import SafeLoader
import pandas as pd
import streamlit_authenticator as stauth
from st_pages import show_pages_from_config, hide_pages
from plot import merge_overlapping_periods

st.set_page_config(layout="wide",
                   page_title='Calendar',)
hide_pages(["Login"])
show_pages_from_config()


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login()
if st.session_state["authentication_status"]:
    with st.sidebar:
        if 'status' not in st.session_state:
            st.session_state['status'] = []
        names = []
        status = st.selectbox('Pick a status:', ['Active', 'Free', 'Busy'])
        for username, info in config['credentials']['usernames'].items():
            names.append(info['name'])
            if info['name'] == st.session_state['name']:
                info['status'] = status
        save_changes = st.button('Save Changes', type='primary')
        authenticator.logout()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Busy days', anchor=False)
        with st.form('busy_days'):
            if 'busy_timeframe' not in st.session_state:
                st.session_state['busy_timeframe'] = []
            col1a, col1b = st.columns(2)
            with col1a:
                start = st.date_input('Pick a starting date', min_value=datetime.now(), max_value=datetime(2024, 12, 31))
                end = st.date_input('Pick an ending date', min_value=datetime.now(), max_value=datetime(2024, 12, 31))
            with col1b:

                add = st.form_submit_button(label="Add")
                pop = st.form_submit_button(label="Pop")
                clear = st.form_submit_button(label="Clear")
            if start and end and add:
                if start > end:
                    st.error('Ending date is sooner than Starting Date')
                else:
                    st.session_state['busy_timeframe'].append((start, end))
            if st.session_state['busy_timeframe'] and pop:
                st.session_state['busy_timeframe'].pop()
            if clear:
                st.session_state['busy_timeframe'] = []
        if st.session_state['busy_timeframe']:
            st.session_state['busy_timeframe'] = merge_overlapping_periods(st.session_state['busy_timeframe'])
            st.write("Recorded busy timeframes:")
            for i, (start_date, end_date) in enumerate(st.session_state['busy_timeframe']):
                st.write(f"`{start_date} - {end_date}`")
    with col2:
        if 'new_task' not in st.session_state:
            st.session_state['new_task'] = []
        st.subheader('Create a new task', anchor=False)
        with st.form('create_tasks'):
            name = st.text_input('Task name:')
            participants = st.multiselect('Select participants:', names)
            deadline = st.date_input('Choose a deadline:', min_value=datetime.now())
            create = st.form_submit_button(label="Create")
            pop = st.form_submit_button(label="Pop")
        if create and name and participants and deadline:
            st.session_state['new_task'].append((name, 0, deadline, participants))
        if st.session_state['new_task'] and pop:
            st.session_state['new_task'].pop()
        if st.session_state['new_task']:
            st.write("Task(s) created:")
            for i, (task_name, task_progress, task_participants, task_deadline) in enumerate(st.session_state['new_task']):
                st.write(f"`{task_name}`")
                st.write(f"Participants: `{task_participants}`")
                st.write(f"Deadline: `{task_deadline}`")
    if save_changes:
        # st.session_state['busy_timeframe'] = []
        # st.session_state['new_task'] = []
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file)
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
