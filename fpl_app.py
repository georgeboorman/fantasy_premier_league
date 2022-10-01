# import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from library import top_performers, player_performance

# Set title
st.title("Fantasy Premier League 20-21")

# Provide context
st.write("This app allows you to analyze [Fantasy Premier League](https://fantasy.premierleague.com/)\n"
         "performance for the 2020-21 season.\n")

# Read in data, clean columns
df = pd.read_csv("datasets/premier_league_player_stats_2020_21.csv")
df = df.drop(columns=['Unnamed: 0'])
df.rename(columns={'name': 'player'}, inplace=True)

# Read in grouped data, clean columns
grouped = pd.read_csv("datasets/premier_league_player_stats_2020_21_grouped.csv")
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

# Plot bar chart based on user input
st.plotly_chart(top_performers(grouped, position_selector, 'total', 10))

# Next interactive element, viewing player performance across season
st.header('Viewing individual player performance')

# User input
player_input = st.selectbox("Choose a player:", grouped['player'].sort_values())

# Plot scatter chart based on user input
st.plotly_chart(player_performance(df, player_input))

# Player total points across season
player_total = df[df['player'] == player_input]['total_points'].sum()

# Show total points for selected player
if player_input:
    st.write("{} had a total of {} fantasy points in the 2020-21 season.".format(player_input, player_total))
