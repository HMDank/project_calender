from plotly_calplot import calplot
import streamlit as st
import numpy as np
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from datetime import datetime, timedelta, date


def create_calender_plot():
    dummy_df = create_schedule_table(st.session_state['busy_timeframe'])

    fig = calplot(dummy_df,
                  name='Busy People',
                  x="ds",
                  y="value",
                  gap=0.5,
                  colorscale = "reds",
                  month_lines_width=3,
                  month_lines_color='#000000',
                  years_as_columns=True,
                  total_height=200)
    fig.update_layout(
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
    )
    return fig


def merge_overlapping_periods(periods):
    sorted_periods = sorted(periods)
    merged_periods = [sorted_periods[0]]
    for current_start, current_end in sorted_periods[1:]:
        last_merged_start, last_merged_end = merged_periods[-1]
        if current_start <= (last_merged_end + timedelta(1)):
            new_start = min(last_merged_start, current_start)
            new_end = max(last_merged_end, current_end)
            merged_periods[-1] = (new_start, new_end)
        else:
            merged_periods.append((current_start, current_end))
    return merged_periods


def create_schedule_table(list):
    # Arrange of calendar
    Begining_date_of_calendar = date(2024, 1, 1)
    Ending_date_of_calendar = date(2024, 12, 31)
    size = (Ending_date_of_calendar - Begining_date_of_calendar).days + 1

    # Set a schedule array
    array = [0]*size

    # Modify a schedule array
    for each in list:
        first_busy_date = each[0]
        last_busy_date = each[1]

        start_index = (first_busy_date - Begining_date_of_calendar).days
        last_index = (last_busy_date - Begining_date_of_calendar).days + 1

        for index in range(start_index, last_index):
            array[index] = 1

    # Make a DataFrame
    Begining_date_of_calendar = Begining_date_of_calendar.strftime('%Y-%m-%d')
    Ending_date_of_calendar = Ending_date_of_calendar.strftime('%Y-%m-%d')
    df = pd.DataFrame({
        "ds": pd.date_range(Begining_date_of_calendar, Ending_date_of_calendar),
        "value": array,
    })

    return df

