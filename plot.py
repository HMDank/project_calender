from plotly_calplot import calplot
import numpy as np
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from datetime import datetime, timedelta


def create_calender_plot():
    dummy_start_date = datetime(2024, 1, 1)
    dummy_end_date = datetime(2024, 12, 31)

    dummy_df = pd.DataFrame({
        "ds": pd.date_range(dummy_start_date, dummy_end_date),
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
    sorted_periods = sorted(periods)
    merged_periods = [sorted_periods[0]]
    for current_start, current_end in sorted_periods[1:]:
        last_merged_start, last_merged_end = merged_periods[-1]
        if current_start <= last_merged_end:
            new_start = min(last_merged_start, current_start)
            new_end = max(last_merged_end, current_end)
            merged_periods[-1] = (new_start, new_end)
        else:
            merged_periods.append((current_start, current_end))
    return merged_periods


def create_progress_table():
    return 0


