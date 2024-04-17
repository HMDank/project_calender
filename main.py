import streamlit as st
import yaml
from yaml.loader import SafeLoader
from plot import create_calender_plot
from st_pages import show_pages_from_config, hide_pages

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

st.header('Group Progress', anchor=False)

plot = create_calender_plot()
st.plotly_chart(plot, use_container_width=True)