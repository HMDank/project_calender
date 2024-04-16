import streamlit as st
from plot import create_calender_plot

st.set_page_config(layout="wide",
                   page_title='Calendar')

plot = create_calender_plot()
st.plotly_chart(plot)

