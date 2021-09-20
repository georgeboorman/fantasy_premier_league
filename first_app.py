# import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Set title
st.title("Fantasy Premier League 20-21")

# Provide context
st.write("This app allows you to analyze [Fantasy Premier League](https://fantasy.premierleague.com/)\n"
         "performance for the 2020-21 season.\n")

# Read in data, clean columns
df = pd.read_csv("premier_league_player_stats_2020_21.csv")
df = df.drop(columns=['Unnamed: 0'])
df.rename(columns={'name': 'player'}, inplace=True)

# Read in grouped data, clean columns
grouped = pd.read_csv("premier_league_player_stats_2020_21_grouped.csv")
grouped = grouped.drop(columns='Unnamed: 0')
grouped['average'] = grouped['average'].round(2)

# Add heading and print top 10 players from grouped
st.write("Top 10 players for the 2020-21 season", grouped.head(10))

# Positions list
positions = ['Goalkeeper', 'Defender', 'Midfielder', 'Striker']

# Selecting best player by position
st.header("Best players by position")

# Input field to choose position for plot
position_selector = st.selectbox("Select position:", positions)

# Function to return figure
def top_performers(df, position, metric, num):
    """
    Function to return a bar plot of top X performing players by specified metric.
    Args:
    :param df: pandas DataFrame for use in function
    :param position: Football position to be analyzed
    :param metric: Statistic to be used for analysis
    :param num: How many players to return
    :return: fig: Figure to be plotted.
    """

    # Subset the data for the position of interest
    data = grouped[grouped['position'] == position].sort_values(metric, ascending=False).head(num)

    # Create the plot and update the layout
    fig = px.bar(x='player', y=metric, data_frame=data, color='team',
                title='Best {}s'.format(position_selector), labels={'total':'points'},
                hover_data={'player':False, 'team':False})
    fig.update_layout(xaxis_title='Player Name', yaxis_title='Fantasy Points')
    return fig

# Plot bar chart based on user input
st.plotly_chart(top_performers(grouped, position_selector, 'total', 10))

# Next interactive element, viewing player performance across season
st.header('Viewing individual player performance')

# User input
player_input = st.selectbox("Choose a player:", grouped['player'].sort_values())

# Function to plot individual player performance across a season
def player_performance(df, player):
    """Function to return a scatter plot of an individual's performance across a season
    Args:
        df: pandas DataFrame for use in function
        player: name of player to put in plot
    Returns: figure to be plotted, total points"""

    # Subset the data for the player of interest
    data = df[df['player'] == player]

    # Create the plot and update the layout
    fig = px.scatter(data_frame=data, x='GW', y='total_points', color='opp_team', 
                    title="{}'s Performance by Game Week".format(player),
                    labels={'opp_team': 'Opponent', 'total_points':'Points', 'GW':'Game Week'})
    fig.update_layout(xaxis_title='Game Week', yaxis_title='Fantasy Points', showlegend=False)
    return fig

# Plot scatter chart based on user input
st.plotly_chart(player_performance(df, player_input))

# Player total points across season
player_total = df[df['player'] == player_input]['total_points'].sum()

# Show total points for selected player
if player_input:
    st.write("{} had a total of {} fantasy points in the 2020-21 season.".format(player_input, player_total))