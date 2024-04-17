import streamlit as st

import streamlit_authenticator as stauth
from plot import create_calender_plot
from st_pages import show_pages_from_config, hide_pages
    
st.set_page_config(layout="wide",
                   page_title='Calendar',)
hide_pages(["Back"])
show_pages_from_config()


with st.sidebar:
    st.subheader('Group Status', anchor=False)
    st.metric('d', 'Dank', label_visibility="collapsed", delta='Active')
    st.metric('m', 'Moi', label_visibility="collapsed", delta='Active')
    st.metric('h', 'Hint', label_visibility="collapsed", delta='Free', delta_color='off')
    st.metric('l', 'Lam', label_visibility="collapsed", delta='Away', delta_color='inverse')

st.header('Group Schedule', anchor=False)

st.header('Group Progress', anchor=False)

plot = create_calender_plot()
st.plotly_chart(plot, use_container_width=True)

