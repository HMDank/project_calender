import streamlit as st
import yaml
from datetime import date, timedelta
from yaml.loader import SafeLoader
import pandas as pd
import streamlit_authenticator as stauth
from st_pages import show_pages_from_config, hide_pages
from plot import merge_overlapping_periods, create_calender_plot, datetime_to_str, str_to_datetime
from database import update_user, retrieve_user_data, add_tasks, retrieve_tasks, update_tasks
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

users_data = retrieve_user_data([user_info["name"] for user_info in config['credentials']['usernames'].values()])
ongoing_tasks = retrieve_tasks()
authenticator.login()
if st.session_state["authentication_status"]:
    tab1, tab2 = st.tabs(['Schedule', 'Ongoing Tasks'])
    with tab1:
        with st.sidebar:
            names = []
            for user_data in users_data:
                names.append(user_data[0]['name'])
                if st.session_state['name'] == user_data[0]['name']:
                    original_status = user_data[0]['status']
                    original_busy_timeframe = str_to_datetime(user_data[0]['schedule'])
                    if user_data[0]['status'] == 'Free':
                        st.metric('d', f"{user_data[0]['name'].capitalize()}", label_visibility="collapsed", delta=f"{user_data[0]['status']}", delta_color='off')
                    elif user_data[0]['status'] == 'Active':
                        st.metric('d', f"{user_data[0]['name'].capitalize()}", label_visibility="collapsed", delta=f"{user_data[0]['status']}", delta_color='normal')
                    else:
                        st.metric('d', f"{user_data[0]['name'].capitalize()}", label_visibility="collapsed", delta=f"{user_data[0]['status']}", delta_color='inverse')
            status = st.selectbox('Status:', ['Active', 'Free', 'Busy'], index=None, placeholder='Update Status', label_visibility='collapsed')
            save_changes = st.button('Save Changes', type='primary')
            authenticator.logout()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Busy days', anchor=False)
            with st.form('busy_days'):
                if 'busy_timeframe' not in st.session_state:
                    st.session_state['busy_timeframe'] = []
                range = st.date_input('Pick a busy range', (date.today(), date.today()), min_value=date.today(), max_value=date(2024, 12, 31))
                col1a, col1b, col1c, col1d = st.columns(4)
                with col1a:
                    add = st.form_submit_button(label="Add", use_container_width=True)
                with col1b:
                    pop = st.form_submit_button(label="Pop", use_container_width=True)
                with col1c:
                    clear = st.form_submit_button(label="Clear", use_container_width=True)
                with col1d:
                    reset = st.form_submit_button(label="Reset", use_container_width=True)
                if range and add:
                    st.session_state['busy_timeframe'].append(range)
                    st.session_state['busy_timeframe'] = merge_overlapping_periods(st.session_state['busy_timeframe'])
                if st.session_state['busy_timeframe'] and pop:
                    st.session_state['busy_timeframe'].pop()
                if clear:
                    st.session_state['busy_timeframe'] = []
                if reset:
                    for user_data in users_data:
                        if st.session_state['name'] == user_data[0]['name']:
                            update_user(user_data[0]['name'], original_status, [[]])
            if st.session_state['busy_timeframe']:
                with col2:
                    st.write("Recorded busy timeframes:")
                    for i, (start_date, end_date) in enumerate(st.session_state['busy_timeframe']):
                        st.write(f"`{start_date} - {end_date}`")
        busy_timeframe = original_busy_timeframe + st.session_state['busy_timeframe'] if original_busy_timeframe[0] else st.session_state['busy_timeframe']
        if busy_timeframe:
            st.plotly_chart(create_calender_plot(merge_overlapping_periods(busy_timeframe)), use_container_width=True)
        else:
            st.plotly_chart(create_calender_plot(busy_timeframe), use_container_width=True)
    with tab2:
        if 'new_task' not in st.session_state:
            st.session_state['new_task'] = []
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Create a new task', anchor=False)
            with st.form('create_tasks'):
                name = st.text_input('Task name:')
                participants = st.multiselect('Select participants:', names)
                deadline = st.date_input('Choose a deadline:', min_value=date.today())
                col1a, col2a = st.columns(2)
                with col1a:
                    add = st.form_submit_button(label="Add", use_container_width=True)
                with col2a:
                    pop = st.form_submit_button(label="Pop", use_container_width=True)
            if add and name and participants and deadline:
                st.session_state['new_task'].append({'name': name,
                                                     'progress': 0,
                                                     'deadline': datetime_to_str(deadline),
                                                     'participants': participants,
                                                     'completed': False})
            if st.session_state['new_task'] and pop:
                st.session_state['new_task'].pop()
            if st.session_state['new_task']:
                st.write("Task(s) created:")
                for i, task in enumerate(st.session_state['new_task']):
                    st.write(f"Task: `{task['name']}`")
                    st.write(f"Participants: `{task['participants']}`")
                    st.write(f"Deadline: `{task['deadline']}`")
        with col2:
            st.subheader('Edit existing task', anchor=False)
            available_task = []
            if 'change_task' not in st.session_state:
                st.session_state['change_task'] = []
            with st.form('edit_tasks'):
                for task in ongoing_tasks:
                    if st.session_state['name'] in task[0]['participants']:
                        available_task.append(task[0])
                name = st.selectbox('Select a Task:', [task[0]['name'] for task[0] in available_task], index=None)
                progress = st.slider('Edit progress', min_value=1, max_value=99)
                col1, col2 = st.columns(2)
                with col1:
                    add = st.form_submit_button(label="Add", use_container_width=True)
                with col2:
                    pop = st.form_submit_button(label="Pop", use_container_width=True)
            if add and name:
                for task in available_task:
                    if name == task['name']:
                        deadline = task['deadline']
                        participants = task['participants']
                st.write("Task(s) Selected:")
                st.session_state['change_task'].append({'name': name,
                                                        'progress': progress,
                                                        'deadline': deadline,
                                                        'participants': participants,
                                                        'completed': False})
            if st.session_state['change_task'] and pop:
                st.session_state['change_task'].pop()
            if st.session_state['change_task']:
                for i, task in enumerate(st.session_state['change_task']):
                    st.write(f"Task: `{task['name']}`")
                    st.write(f"Progress: `{task['progress']}`")
                    st.write(f"Participants: `{task['participants']}`")
                    st.write(f"Deadline: `{task['deadline']}`")
    if not status:
        status = original_status
    if save_changes:
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file)
        if not status:
            status = original_status
        converted_busy_timeframe = []
        for sublist in merge_overlapping_periods(busy_timeframe):
            converted_sublist = []
            for item in sublist:
                converted_sublist.append(datetime_to_str(item))
            converted_busy_timeframe.append(converted_sublist)
        update_user(st.session_state['name'], status, converted_busy_timeframe)
        add_tasks(st.session_state['new_task'])
        update_tasks(st.session_state['change_task'])
        st.session_state['busy_timeframe'] = []
        st.session_state['new_task'] = []
        st.session_state['change_task'] = []
        with st.sidebar:
            st.success('Successfully saved changes!')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
