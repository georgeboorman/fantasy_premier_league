"""
Python file containing all functions required for the Streamlit app fantasy_premier_league.py
"""

# import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px

def top_performers(df, position, metric, num):
    """
    Function to return a bar plot of top X performing players by specified metric.
    Args:
      df: pandas DataFrame for use in function
      position: Football position to be analyzed
      metric: Statistic to be used for analysis
      num: How many players to return
    Returns: Figure to be plotted.
    """

    # Subset the data for the position of interest
    data = df[df['position'] == position].sort_values(metric, ascending=False).head(num)

    # Create the plot and update the layout
    fig = px.bar(x='player', y=metric, data_frame=data, color='team',
                title=f'Best {position_selector}s'.format(position_selector), labels={'total':'points'},
                hover_data={'player':False, 'team':False})
    fig.update_layout(xaxis_title='Player Name', yaxis_title='Fantasy Points')
    return fig
  
def player_performance(df, player):
    """Function to return a scatter plot of an individual's performance across a season
    Args:
        df: pandas DataFrame for use in function
        player: name of player to put in plot
    Returns: Figure to be plotted, total points"""

    # Subset the data for the player of interest
    data = df[df['player'] == player]

    # Create the plot and update the layout
    fig = px.scatter(data_frame=data, x='GW', y='total_points', color='opp_team', 
                    title=f"{player}'s Performance by Game Week",
                    labels={'opp_team': 'Opponent', 'total_points':'Points', 'GW':'Game Week'})
    fig.update_layout(xaxis_title='Game Week', yaxis_title='Fantasy Points', showlegend=False)
    return fig
