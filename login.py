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
with open('tasks.yaml', 'r') as file:
    ongoing_tasks = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

st.session_state['busy'] = []

authenticator.login()
if st.session_state["authentication_status"]:
    tab1, tab2 = st.tabs(['Schedule', 'Ongoing Tasks'])
    with tab1:
        with st.sidebar:
            if 'status' not in st.session_state:
                st.session_state['status'] = []
            names = []
            for username, info in config['credentials']['usernames'].items():
                names.append(info['name'])
                if info['name'] == st.session_state['name']:
                    if info['status'] == 'Free':
                        st.metric('d', f"{st.session_state['name']}", label_visibility="collapsed", delta=f"{info['status']}", delta_color='off')
                    elif info['status'] == 'Active':
                        st.metric('d', f"{st.session_state['name']}", label_visibility="collapsed", delta=f"{info['status']}", delta_color='normal')
                    else:
                        st.metric('d', f"{st.session_state['name']}", label_visibility="collapsed", delta=f"{info['status']}", delta_color='inverse')
                    status = st.selectbox('Status:', ['Active', 'Free', 'Busy'], index=None, placeholder='Update Status', label_visibility='collapsed')
                    if status and info['name'] == st.session_state['name']:
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
                with col2:
                    st.write("Recorded busy timeframes:")
                    for i, (start_date, end_date) in enumerate(st.session_state['busy_timeframe']):
                        st.write(f"`{start_date} - {end_date}`")
    with tab2:
        if 'new_task' not in st.session_state:
            st.session_state['new_task'] = []
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Create a new task', anchor=False)
            with st.form('create_tasks'):
                name = st.text_input('Task name:')
                participants = st.multiselect('Select participants:', names)
                deadline = st.date_input('Choose a deadline:', min_value=datetime.now())
                col1a, col2a = st.columns(2)
                with col1a:
                    add = st.form_submit_button(label="Add", use_container_width=True)
                with col2a:
                    pop = st.form_submit_button(label="Pop", use_container_width=True)
            if add and name and participants and deadline:
                st.session_state['new_task'].append({'task': name,
                                                    'progress': 0,
                                                    'deadline': deadline,
                                                    'participants': participants,
                                                    'completed': False})
            if st.session_state['new_task'] and pop:
                st.session_state['new_task'].pop()
            if st.session_state['new_task']:
                st.write("Task(s) created:")
                for i, task in enumerate(st.session_state['new_task']):
                    st.write(f"Task: `{task['task']}`")
                    st.write(f"Participants: `{task['participants']}`")
                    st.write(f"Deadline: `{task['deadline']}`")
        with col2:
            st.subheader('Edit existing task', anchor=False)
            available_task = []
            if 'change_task' not in st.session_state:
                st.session_state['change_task'] = []
            with st.form('edit_tasks'):
                for task in ongoing_tasks:
                    if st.session_state['name'] in task['participants']:
                        available_task.append(task)
                name = st.selectbox('Select a Task:', [task['task'] for task in available_task], index=None)
                progress = st.slider('Edit progress', min_value=1, max_value=99)
                col1, col2 = st.columns(2)
                with col1:
                    add = st.form_submit_button(label="Add", use_container_width=True)
                with col2:
                    pop = st.form_submit_button(label="Pop", use_container_width=True)
            if add and name:
                for task in available_task:
                    if name == task['task']:
                        deadline = task['deadline']
                        participants = task['participants']
                st.write("Task(s) Selected:")
                st.session_state['change_task'].append({'task': name,
                                                        'progress': progress,
                                                        'deadline': deadline,
                                                        'participants': participants,
                                                        'completed': False})
            if st.session_state['change_task'] and pop:
                st.session_state['change_task'].pop()
            if st.session_state['change_task']:
                for i, task in enumerate(st.session_state['change_task']):
                    st.write(f"Task: `{task['task']}`")
                    st.write(f"Progress: `{task['progress']}`")
                    st.write(f"Participants: `{task['participants']}`")
                    st.write(f"Deadline: `{task['deadline']}`")
    if save_changes:
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file)
        if ongoing_tasks:
            updated_task = []
            subset_lookup = {d['task']: d for d in st.session_state['change_task'] if 'task' in d}
            for idx, d in enumerate(ongoing_tasks):
                if 'task' in d and d['task'] in subset_lookup:
                    ongoing_tasks[idx] = subset_lookup[d['task']]
            ongoing_tasks.extend(st.session_state['new_task'])
        else:
            ongoing_tasks = st.session_state['new_task']
        with open('tasks.yaml', 'w') as task_file:
            yaml.dump(ongoing_tasks, task_file, default_flow_style=False)
        st.session_state['busy_timeframe'] = []
        st.session_state['new_task'] = []
        st.session_state['change_task'] = []
        with st.sidebar:
            st.success('Successfully saved changes!')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
