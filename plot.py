from plotly_calplot import calplot
import numpy as np
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from datetime import datetime, timedelta

with open('busy.yaml') as file:
    busy = yaml.load(file, Loader=SafeLoader)

start_busy_day = []
end_busy_day = []
name = []

if busy:
    for entry in busy:
        start_busy_day.append(entry['start_busy_day'])
        end_busy_day.append(entry['end_busy_day'])
        name.append(entry['name'])


def create_calender_plot():
    dummy_start_date = datetime(2024, 1, 1)
    dummy_end_date = datetime(2024, 12, 31)

    dummy_df = pd.DataFrame({
        "ds": pd.date_range(dummy_start_date, dummy_end_date),
        #Khó VCL
        "value": 0
    })

    fig = calplot(dummy_df,
                name='Busy People',
                x="ds",
                y="value",
                gap=0,
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
    # Sort periods based on the start date (first element of each tuple)
    sorted_periods = sorted(periods)

    # Initialize result list with the first period
    merged_periods = [sorted_periods[0]]

    # Iterate through sorted periods starting from the second period
    for current_start, current_end in sorted_periods[1:]:
        last_merged_start, last_merged_end = merged_periods[-1]

        # Check if the current period overlaps with the last merged period
        if current_start <= last_merged_end:  # Overlapping or contiguous
            # Merge the periods by taking the earliest start and latest end
            new_start = min(last_merged_start, current_start)
            new_end = max(last_merged_end, current_end)
            merged_periods[-1] = (new_start, new_end)  # Update last merged period
        else:
            # No overlap, add the current period to the result
            merged_periods.append((current_start, current_end))

    return merged_periods


def create_progress_table():
    return 0


