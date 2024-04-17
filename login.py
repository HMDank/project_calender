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
    start = st.date_input('Pick a starting date', min_value=datetime(2024, 1, 1), max_value=datetime(2024, 12, 31))
    end = st.date_input('Pick an ending date', min_value=datetime(2024, 1, 1), max_value=datetime(2024, 12, 31))
    st.write(start, end)
    submit = st.button('Save')

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')