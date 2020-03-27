import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from datetime import date
from os import environ
from pathlib import Path
from pandas.plotting import register_matplotlib_converters


def plot_nyt_covid_data(state):
    # Read in data from csv and get needed parameters
    state = state.title()
    df = pd.read_csv(
        'https://raw.githubusercontent.com/nytimes/covid-19-data/master/' +
        'us-states.csv')
    if df.empty:
        print('No data available! Double-check state name.')
        return
    today = date.today().strftime('%Y%m%d')

    # Get all data from the state desired
    is_state = df['state'] == state
    df = df[is_state]
    earliest_date = df.iloc[0][0]
    latest_date = df.iloc[-1][0]
    print(f'Data current as of {latest_date}', flush=True)

    # Plot data
    register_matplotlib_converters()
    fig, ax = plt.subplots(figsize=(8, 8))
    date_form = mdates.DateFormatter('%m-%d')
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(date_form)
    ax.scatter(df['date'], df['cases'], color='tab:red')
    ax.text(0.2, 0.95, f'Data current as of {latest_date}',
            horizontalalignment='center',
            fontsize=8, transform=ax.transAxes,
            color='black')
    plt.grid(axis='y')

    # Set title and labels for axes
    ax.set(xlabel="Date",
           ylabel="Number of Cases",
           title=f"Total Number of Confirmed COVID-19 Cases in {state}")
    ax.set_xlim(left=earliest_date, right=latest_date)

    # Save the plots to file. If state with two words replace spaces
    state = state.replace(' ', '_')
    save_dir = Path(environ['HOME'], f'covid/images/{today}/')
    if not Path.exists(save_dir):
        os.mkdir(save_dir)
    plt.savefig(str(save_dir) + f'/{state}.png')
    print(f'Writing: {save_dir}' + f'/{state}.png', flush=True)


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('state', help='State of which data is requested. \
                            Replace spaces in multi-word states with \
                            underlines (ex: new_york)')
        args = parser.parse_args()
        state = args.state
        state = state.replace('_', ' ')
        plot_nyt_covid_data(state)
    except KeyError:
        print('Invalid state name given')
