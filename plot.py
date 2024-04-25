from plotly_calplot import calplot
import streamlit as st
import numpy as np
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from datetime import datetime, timedelta, date


def create_calender_plot(busy_list):
    dummy_df = create_schedule_table(busy_list)

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
    merged_periods = [periods[0]]
    for current_start, current_end in periods[1:]:
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


def datetime_to_str(dt):
    if isinstance(dt, date):
        return dt.isoformat()
    return dt


def str_to_datetime(list_of_lists):
    converted_lists = []

    for inner_list in list_of_lists:
        converted_inner_list = []
        for date_str in inner_list:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            converted_inner_list.append(date_obj)
        converted_lists.append(converted_inner_list)

    return converted_lists


def create_dataframe(users_data):
    start_date = date.today()
    end_date = date(2024, 12, 31)
    date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    # Initialize an empty DataFrame
    columns = ['Name'] + [date.strftime('%Y-%m-%d') for date in date_range]
    df = pd.DataFrame(columns=columns)
    user_rows = []
    # Loop through users_data and populate the DataFrame
    for user_data in users_data:
        name = user_data[0]['name']
        schedule = user_data[0]['schedule']

        user_row = {'Name': name}

        for day in date_range:
            user_row[day.strftime('%Y-%m-%d')] = 'Free'
        for busy_range in schedule:
            if busy_range:
                start_date_str = busy_range[0]
                end_date_str = busy_range[1]
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                current_date = start_date
                while current_date <= end_date:
                    user_row[current_date.strftime('%Y-%m-%d')] = 'Busy'
                    current_date += timedelta(days=1)
        user_rows.append(pd.DataFrame([user_row]))

    df = pd.concat(user_rows, ignore_index=True)
    df.set_index('Name', inplace=True)
    return df

