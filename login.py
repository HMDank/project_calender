import streamlit as st
import yaml
from datetime import datetime
from yaml.loader import SafeLoader
import pandas as pd
import streamlit_authenticator as stauth
from st_pages import show_pages_from_config, hide_pages

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
        authenticator.logout()
        if 'status' not in st.session_state:
            st.session_state['status'] = []
        names = []
        status = st.selectbox('Pick a status:', ['Active', 'Free', 'Busy'])
        for username, info in config['credentials']['usernames'].items():
            names.append(info['name'])
            if info['name'] == st.session_state['name']:
                info['status'] = status
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Busy days', anchor=False)
        with st.form('busy_days'):
            col1a, col1b = st.columns(2)
            with col1a:
                start = st.date_input('Pick a starting date', min_value=datetime.now(), max_value=datetime(2024, 12, 31))
            with col1b:
                end = st.date_input('Pick an ending date', min_value=start, max_value=datetime(2024, 12, 31))
            if 'busy_timeframe' not in st.session_state:
                st.session_state['busy_timeframe'] = []
            add = st.form_submit_button(label="Add")
            undo = st.form_submit_button(label="Undo")
            if start and end and add:
                st.session_state['busy_timeframe'].append((start, end))
            if undo:
                st.session_state['busy_timeframe'].pop()
        if st.session_state['busy_timeframe']:
            st.write("You are busy in these timeframes:")
            for i, (start_date, end_date) in enumerate(st.session_state['busy_timeframe']):
                st.write(f"{start_date} - {end_date}")
            st.write(st.session_state['busy_timeframe'])
    with col2:
        st.subheader('Create a new task', anchor=False)
        with st.form('create_tasks'):
            name = st.text_input('Task name:')
            participants = st.multiselect('Select participants:', names)
            deadline = st.date_input('Choose a deadline:', min_value=datetime.now())
            create = st.form_submit_button(label="Create")
        if create:
            st.write('0')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
