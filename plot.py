from plotly_calplot import calplot
import numpy as np
import pandas as pd


def create_calender_plot():
    dummy_start_date = "2024-01-01"
    dummy_end_date = "2024-12-31"
    # date range from start date to end date and random
    # column named value using amount of days as shape
    dummy_df = pd.DataFrame({
        "ds": pd.date_range(dummy_start_date, dummy_end_date),
        "value": np.random.randint(low=0, high=30,
        size=(pd.to_datetime(dummy_end_date) - pd.to_datetime(dummy_start_date)).days + 1,),
    })

    fig = calplot(dummy_df,
                  name='Busy People',
                  x="ds",
                  y="value",
                  gap=0,
                  month_lines_width=3,
                  month_lines_color='#FFFFFF',
                  years_as_columns=True,
                  total_height=200)
    fig.update_layout(
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
    )
    return fig


def create_progress_table():
    return 0
