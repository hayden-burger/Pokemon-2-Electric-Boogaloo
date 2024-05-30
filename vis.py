"""
This script is created by Hayden Burger, Corinne Desroches, and David Lee 
with additional assistance provided through GitHub Copilot.

Description:
    This script builds a streamlit dashboard to visualize the results of 
    generation 1 pokemon battles. Every pokemon battles every other pokemon
    and the win tally is recorded in a dataframe which is exported to 1000runs.csv.
    The pokemon stats and win tallys are compared and visualized.
    The performance of a single pokemon can be visualized as well as the performance
    of a team of pokemon against the elite four.
"""
# import statements
import streamlit as st
import pandas as pd
import plotly.express as px
# import plotly.graph_objects as go   # Used for plotting scatterplot with sprites - takes forever to load
import pokemon_module as pk
import numpy as np
import io
import os
from contextlib import redirect_stdout
import ast
from tabulate import tabulate
import copy

@st.cache_data  # Corrected decorator for caching data

# function to load the data
def load_data(filepath, **kwargs):
    if filepath.endswith('.xlsx'):
        return pd.read_excel(filepath, **kwargs)
    elif filepath.endswith('.csv'):
        return pd.read_csv(filepath, **kwargs)
    else:
        raise ValueError("Unsupported file format. Please use a CSV or XLSX file.")

# import the data from the pokemon_module
pokemon_data = pk.Pokemon_df
move_data = pk.merged_moves_df
# read all sheets from the elite_results.xlsx file
team_data = load_data('elite_results.xlsx', sheet_name = None, index_col=0)  

# Adjust the path to your file
file_options_wins = {'Level 1 data': 'Output_data_files/Level_1_1000runs.csv'}  # Dictionary of file options
# extend file options to include all files in the directory 'Output_data_files'
for file in os.listdir('Output_data_files'):
    if file.endswith('wins.csv'):
        file_path = os.path.join('Output_data_files', file)
        file_name = file.replace('wins.csv', '')  # Replace 'wins.csv' with ' data' in the file name
        file_name = file_name.replace('100runs', 'Level 50: ')
        file_name = file_name.replace('hp', ' % HP ')
        file_name = file_name.replace('_', '')
        file_name = file_name.replace('P ', 'P with ')
        file_options_wins[file_name] = file_path

file_options_health = {}
for file in os.listdir('Output_data_files'):
    if file.endswith('health.csv'):
        file_path = os.path.join('Output_data_files', file)
        file_name = file.replace('health.csv', '')  # Replace 'wins.csv' with ' data' in the file name
        file_name = file_name.replace('100runs', 'Level 50: ')
        file_name = file_name.replace('hp', ' % HP ')
        file_name = file_name.replace('_', '')
        file_name = file_name.replace('P ', 'P with ')
        file_options_health[file_name] = file_path

file_options_times = {}
for file in os.listdir('Output_data_files'):
    if file.endswith('times.csv'):
        file_path = os.path.join('Output_data_files', file)
        file_name = file.replace('times.csv', '')
        file_name = file_name.replace('100runs', 'Level 50: ')
        file_name = file_name.replace('hp', ' % HP ')
        file_name = file_name.replace('_', '')
        file_name = file_name.replace('P ', 'P with ')
        file_options_times[file_name] = file_path

# Color mapping for Pokémon types
type_colors = {
    'grass': '#78C850',   # Green
    'fire': '#F08030',    # Red
    'water': '#6890F0',   # Blue
    'bug': '#A8B820',     # Olive
    'normal': '#A8A878',  # Khaki
    'poison': '#A040A0',  # Purple
    'electric': '#F8D030',# Yellow
    'ground': '#E0C068',  # Pale Brown
    'fairy': '#EE99AC',   # Pink
    'fighting': '#C03028',# Crimson
    'psychic': '#F85888', # Light Crimson
    'rock': '#B8A038',    # Bronze
    'ghost': '#705898',   # Dark Purple
    'ice': '#98D8D8',     # Pale Cyan
    'dragon': '#7038F8',  # Royal Blue
}

# create a dictionary of pokemon objects
pk_dict = pk.create_pokemon_dict()
# create a series of list of pokemon objects for each Elite Four Team
elite4_1 = ['dewgong','cloyster','slowbro','jynx','lapras']
elite4_2 = ['onix','hitmonlee','hitmonchan','onix','machamp']
elite4_3 = ['gengar','golbat','haunter','arbok','gengar']
elite4_4 = ['gyarados','dragonair','dragonair','aerodactyl','dragonite']
elite_list = [elite4_1,elite4_2,elite4_3,elite4_4]
elite = []
for team in elite_list:
    elite.append(pk.create_pokemon_objects(team))
elite_dict = {'Lorelei': elite_list[0], 'Bruno': elite_list[1], 'Agatha': elite_list[2], 'Lance': elite_list[3]}
 # URLs to the images
elite_four_images = {
    "Lorelei": "https://img.pokemondb.net/sprites/trainers/red-blue/lorelei.png",
    "Bruno": "https://img.pokemondb.net/sprites/trainers/red-blue/bruno.png",
    "Agatha": "https://img.pokemondb.net/sprites/trainers/red-blue/agatha.png",
    "Lance": "https://img.pokemondb.net/sprites/trainers/red-blue/lance.png"
}
# team members for each team
team1 = ['gyarados','gyarados','gyarados','gyarados','gyarados','gyarados']
team2 = ['gengar','gengar','gengar','gengar','gengar','gengar']
team3 = ['articuno','zapdos','mewtwo','blastoise','mew','moltres']
team4 = ['gengar','poliwrath','magneton','dragonite','charizard','alakazam']
team5 = ['poliwrath','hitmonchan','machamp','machamp','primeape','hitmonlee']
team6 = ['mewtwo','snorlax','muk','vaporeon','wigglytuff','chansey']
team7 = ['gengar','gyarados','articuno','haunter','zapdos','mewtwo']
team8 = ['gengar','articuno','mewtwo','exeggutor','clefable','vaporeon']
team9 = ['articuno','zapdos','moltres',"dodrio","farfetch'd",'pidgeot']
team10 = ['gengar','lapras','rhydon','venusaur','onix','growlithe']
team11 = ['exeggutor','gengar','vaporeon','clefable','mewtwo','articuno']
teamslist = [team1,team2,team3,team4,team5,team6,team7,team8,team9,team10,team11]
# convert teamslist to dictionary with keys as team names and values as team members
teams_dict = {}
for i in range(len(teamslist)):
    teams_dict['team' + str(i+1)] = teamslist[i]
# teams in reverse order have an additional b at the end
teamsreverse = copy.deepcopy(teamslist)
for i in range(len(teamslist)):
    teamsreverse[i].reverse()
    teams_dict['team' + str(i+1) + 'b'] = teamsreverse[i]

attrs = ['base_total', 'hp', 'speed', 'attack', 'defense', 'sp_attack', 'sp_defense']
# Sum up stats for each pokemon in the team and store in a dataframe
team_stat_df = pd.DataFrame()
for attr in attrs:
    for team in teams_dict.keys():
        team_stat_df.loc[team, attr] = sum([pokemon_data.loc[pokemon, attr] for pokemon in teams_dict[team]])


# Function to get color based on Pokémon types
def get_pokemon_color(type1, type2, other_type1, other_type2):
    # Set the default/fallback color
    fallback_color = '#A0A0A0' # Grey as the default color

    # First, set the color for the first Pokémon
    color_pokemon1 = type_colors.get(type1, fallback_color)

    # Now, determine the color for the second Pokémon
    if other_type1 != type1:
        color_pokemon2 = type_colors.get(other_type1, fallback_color)
    elif other_type2 and other_type2 != type1 and other_type2 != type2:
        color_pokemon2 = type_colors.get(other_type2, fallback_color)
    else:
        color_pokemon2 = fallback_color

    # If both Pokémon end up with the same color, assign the fallback color to the second Pokémon
    if color_pokemon1 == color_pokemon2:
        color_pokemon2 = fallback_color

    return color_pokemon1, color_pokemon2


#Assign all pokemon as a class
def assign_pokemon_class():
    gen1 = np.where(pk.Pokemon_df['generation'] == 1) #isolates gen 1 pokemon
    pokemon_dict = {} #Dictionary in {Pokemon name:Pokemon class format}
    for pokemon_name in pk.Pokemon_df.iloc[gen1].index: #for every pokemon in gen 1
        #assign a class as a member of the dictionary
        pokemon_dict[pokemon_name] = pk.Pokemon(pokemon_name)
    return pokemon_dict


# New function to plot total wins histogram over every pokemon
def plot_total_wins(battle_data):
    fig_total_wins = px.bar(total_wins, x='name', y='Total Wins',
                            title='Total Wins per Pokémon')
    fig_total_wins.update_layout(xaxis_title='Pokémon', yaxis_title='Number of Wins')
    st.plotly_chart(fig_total_wins)
    
    
# Function to plot a scatterplot of Pokémon base_total
def plot_total_wins_vs_attribute(merged_data, attribute):
    fig_scatter = px.scatter(merged_data, x='Total Wins', y=attribute, text='name',
                     title=f"Pokémon Total Wins vs. {attribute.capitalize()}", 
                     hover_data=['type1', 'type2'])
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.update_layout(height=600, xaxis_title='Total Wins', yaxis_title=attribute.capitalize())
    st.plotly_chart(fig_scatter)

# Function to plot a scatterplot of Pokémon team total attributes vs. metrics
def plot_team_wins_vs_attribute(merged_data, attribute, metric):
    fig_scatter = px.scatter(merged_data, x=metric, y=attribute, text='Team',
                     title=f"Pokémon {metric.capitalize()} vs. {attribute.capitalize()}")
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.update_layout(height=600, xaxis_title=metric.capitalize(), yaxis_title=attribute.capitalize())
    st.plotly_chart(fig_scatter)


    # code below is for messing with sprites for the pokemon. Slows the performance of the dashboard
    # due to the for loop iteration. Left in here for future work...

    # # Initialize a figure
    # fig = go.Figure()

    # # Add scatter plot points for context
    # fig.add_trace(go.Scatter(
    #     x=merged_data['Total Wins'], 
    #     y=merged_data[attribute], 
    #     mode='markers',  # This ensures we have dots as markers; customize as needed
    #     marker=dict(size=1, color='LightSkyBlue'),  # Adjust color and size as necessary
    #     text=merged_data['name'],  # Sets the hover text to Pokémon name
    #     hoverinfo='text'  # Hover shows Pokémon name; customize as needed
    # ))

    # # Iterate through the merged data to add each Pokémon as an image with custom x, y coordinates
    # for index, row in merged_data.iterrows():
    #     fig.add_layout_image(
            
    #         source=row['image_url'],
    #         xref="x",
    #         yref="y",
    #         x=row['Total Wins'],
    #         y=row[attribute],
    #         sizex=5000,  # Adjust size as necessary; consider plot scale
    #         sizey=100,  # Adjust size as necessary; consider plot scale
    #         xanchor="center",
    #         yanchor="middle",
    #         opacity=0.8  # Adjust for desired transparency
            
    #     )

    # # Set axes and layout properties
    # fig.update_xaxes(title='Total Wins')
    # fig.update_yaxes(title=attribute.capitalize())
    # fig.update_layout(height=600, title=f"Pokémon Total Wins vs. {attribute.capitalize()}")
    
    # # Disable the default scatter plot legend
    # fig.update_layout(showlegend=False)

    # # Adjust layout images to be behind scatter points
    # fig.update_layout_images(layer="below")

    # st.plotly_chart(fig)
    

# function for plotting the performance of a single pokemon
def plot_performance(selected_pokemon):
    performance_data = battle_data.loc[selected_pokemon,:].copy()
    performance_data = performance_data.sort_values(ascending=False)
    
    fig_performance = px.bar(performance_data, y=performance_data.values,
                                title=f'Performance Scores for {selected_pokemon}')
    fig_performance.update_layout(xaxis_title='Opponent', yaxis_title='Number of Wins')
    st.plotly_chart(fig_performance)

# Function to display Pokémon details in a compact card format
def display_pokemon_details(column, pokemon_name):
    # Retrieve Pokémon details
    details = pokemon_data.loc[pokemon_name, ['generation', 'type1', 'type2', 'height_m', 'weight_kg', 'pokedex_number', 'image_url']]
    moves = move_data.loc[move_data['name'].isin([pokemon_name])].move
    html_content = f"""
                    <img src="{details['image_url']}" width="100"><br>
                    <b style='font-size: 20px;'>{pokemon_name}</b><br>
                    Pokedex#: {details['pokedex_number']}<br>
                    Gen: {details['generation']}<br>
                    T1: {details['type1']}<br>
                    """
    if pd.notnull(details['type2']):  # Check if 'type2' is not NaN
        html_content += f"T2: {details['type2']}<br>"
    html_content += f"""Ht: {details['height_m']} m<br>
                    Wt: {details['weight_kg']} kg    
                    <b>Moves:</b>
                    <ul>
                    """
    for move in moves.values:
        html_content += f"<li>{move}</li>"
    html_content += "</ul>"
    # Display details in the specified column
    with column:
        st.markdown(html_content, unsafe_allow_html=True)

# Comparison function with color coding integration
def compare_pokemon(column, pokemon1, pokemon2, pokemon1_color, pokemon2_color, max_base_total):
    attrs = ['base_total', 'hp', 'speed', 'attack', 'defense', 'sp_attack', 'sp_defense']
    pokemon1_data = pokemon_data.loc[pokemon1, attrs]
    pokemon2_data = pokemon_data.loc[pokemon2, attrs]
    
    comparison_data = pd.DataFrame({'Attribute': attrs, pokemon1: pokemon1_data, pokemon2: pokemon2_data}).melt(id_vars='Attribute', var_name='Pokemon', value_name='Value')

    with column:
        fig_comparison = px.bar(comparison_data, x='Attribute', y='Value', color='Pokemon', barmode='group', title=f'Comparison: {pokemon1} vs. {pokemon2}',
                                color_discrete_map={pokemon1: pokemon1_color, pokemon2: pokemon2_color})
        fig_comparison.update_layout(yaxis=dict(range=[0, max_base_total]), width = 450)
        fig_comparison.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    xaxis=dict(showline=True, linecolor='rgb(204, 204, 204)', linewidth=2),
                                    yaxis=dict(showline=True, linecolor='rgb(204, 204, 204)', linewidth=2),
                                    legend=dict(x=1, y=1, xanchor='right', yanchor='top'))
        st.plotly_chart(fig_comparison)

def compare_teams(column, team1, team2, team1_color, team2_color, max_base_total):
    attrs = ['base_total', 'hp', 'speed', 'attack', 'defense', 'sp_attack', 'sp_defense']
    team1_data = pd.DataFrame()
    team2_data = pd.DataFrame()
    # get total stats for each pokemon in the team
    for attr in attrs:
        team1_data[attr] = [pokemon_data.loc[pokemon, attr] for pokemon in team1]
        team2_data[attr] = [pokemon_data.loc[pokemon, attr] for pokemon in team2]
    team1_total = team1_data.sum()
    team2_total = team2_data.sum()
    comparison_data = pd.DataFrame({'Attribute': attrs, 'Team 1': team1_total, 'Team 2': team2_total}).melt(id_vars='Attribute', var_name='Team', value_name='Value')
    
    with column:
        fig_comparison = px.bar(comparison_data, x='Attribute', y='Value', color='Team', barmode='group', title=f'Team Total Stats Comparison',
                                color_discrete_map={'Team 1': team1_color, 'Team 2': team2_color})
        fig_comparison.update_layout(yaxis=dict(range=[0, max_base_total]), width = 450)
        fig_comparison.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    xaxis=dict(showline=True, linecolor='rgb(204, 204, 204)', linewidth=2),
                                    yaxis=dict(showline=True, linecolor='rgb(204, 204, 204)', linewidth=2),
                                    legend=dict(x=1, y=1, xanchor='right', yanchor='top'))
        st.plotly_chart(fig_comparison)

def all_teams_results(team_battles):    
    # get the total wins and times for all teams
    total_wins = []
    avg_times = []
    enemy_dict = []
    for team in team_battles.keys():
        wins, times, enemy = get_total_wins_and_times(team_battles[team])
        total_wins.append(wins)
        # get the average time and if there are no wins, set the average time to 0
        avg_time = round(np.mean(times),2) if len(times) > 0 else 0
        avg_times.append(avg_time)
        enemy_dict.append(enemy)
    return total_wins, avg_times, enemy_dict

# plot the total wins and sort by total wins
def plot_battle_wins(total_wins, team_battles, list_member_names):
    team_names = list(team_battles.keys())
    team_wins = pd.DataFrame({'Team': team_names, 'Wins': total_wins, 'Members': list_member_names})
    team_wins = team_wins.sort_values(by='Wins', ascending=False)
    fig_team_wins = px.bar(team_wins, x='Team', y='Wins', text='Wins', title='Total Wins for Each Team')
    fig_team_wins.update_layout(xaxis_title='Team', yaxis_title='Total Wins')
    # Add a hover tooltip for the team members
    fig_team_wins.update_traces(hovertemplate='<b>%{x}: %{text}</b><br>%{y} Wins<br>', text=team_wins['Members'])
    st.plotly_chart(fig_team_wins)
    
# plot the total times and sort by total wins
def plot_battle_times(avg_times, total_wins, team_battles, list_member_names):
    team_names = list(team_battles.keys())
    team_times = pd.DataFrame({'Team': team_names, 'Avg Time': avg_times, 'Members': list_member_names, 'Wins': total_wins})
    team_times = team_times.sort_values(by='Wins', ascending=False)
    fig_team_times = px.bar(team_times, x='Team', y='Avg Time', text='Avg Time', title='Average Time for Each Team')
    fig_team_times.update_layout(xaxis_title='Team', yaxis_title='Average Time (m)')
    # Add a hover tooltip for the team members
    fig_team_times.update_traces(hovertemplate='<b>%{x}: %{text}m</b><br>%{y} Avg Time<br>', text=team_times['Members'])
    st.plotly_chart(fig_team_times)
    

def get_total_wins_and_times(team_results):
    total_wins = team_results['Result'].sum()
    times = team_results.loc[team_results['Result'] == 1, 'Time'].tolist()
    enemy_dict = dict(team_results.loc[team_results['Result'] == 0, 'Winner'].value_counts())
    return [total_wins, times, enemy_dict]

def plot_times(times, team_name):
    fig_times = px.histogram(x=times, title=f'Time Taken for {team_name} to Defeat the Elite Four')
    fig_times.update_xaxes(title='Time (m)')
    fig_times.update_yaxes(title='frequency')
    fig_times.update_layout(showlegend=False)
    st.plotly_chart(fig_times)

# Create a list of pages for the Streamlit app
pages = [
    "Total Wins",
    "Battle Performance",
    "Pokémon Stats",
    "Team Battle Data",
    "Pick a Team"
]
page1, page2, page3, page4, page5 = st.tabs(pages)




# Page 1: Total Wins
with page1:
    st.title('Pokémon Battle Performance')
    
    # Add App description
    with st.expander("App Description"):
        st.markdown("""
                    ## Simulation Overview

                    This app showcases the results of 1,000 Monte Carlo simulated runs of each Generation 1 Pokémon battling against each other. With 151 Pokémon, the wins were recorded in a pandas dataframe of size 151x151, where each cell takes a value between 0 and 1000, representing the number of wins Pokémon A has against Pokémon B.

                    ### Assumptions/Restrictions

                    For our simulation, we made the following assumptions/restrictions:

                    - Every Pokémon was at level 1.
                    - Each Pokémon only has access to moves it knows at level 1.
                    - Each move is randomly selected on its turn if it has access to it.
                    - PP for moves was not included; instead, we called it a draw after 100 rounds of combat.
                    """, unsafe_allow_html=False)
        
    # Calculate total wins for each Pokémon
    battle_data_key = st.selectbox('Select a win data file:', options=file_options_wins, key='file_select')  # Dropdown menu for file selection
    battle_data = load_data(file_options_wins[battle_data_key], index_col='name')
    total_wins = battle_data.sum(axis=1).sort_values(ascending=False).reset_index()
    total_wins.columns = ['name', 'Total Wins']  # Renaming for clarity
    # Merge total wins with pokemon_data on the Pokémon name
    merged_data = pd.merge(pokemon_data.reset_index(), total_wins, on='name')
    
    st.write("---")  # Add a separator
    plot_total_wins(battle_data)
    st.write("---")  # Adds a visual separator

    # Allow user to select an attribute to compare against Total Wins
    attribute_options = ['type1', 'type2', 'base_total', 'hp', 'speed', 'attack', 'defense', 'sp_attack', 'sp_defense'] # Assuming 'name' is not in pokemon_data columns
    selected_attribute = st.selectbox("Select an attribute to compare with Total Wins:", options=attribute_options, key='attribute_select_1')
    plot_total_wins_vs_attribute(merged_data, selected_attribute)
    st.write("---")  # Add a separator for visual clarity

# Page 2: Selected Pokémon Performance
with page2:
    st.title('Individual Pokémon Battle Performance')
    # Calculate total wins for each Pokémon
    battle_data_key = st.selectbox('Select a win data file:', options=file_options_wins, key='file_select2')  # Dropdown menu for file selection
    battle_data = load_data(file_options_wins[battle_data_key], index_col='name')
    total_wins = battle_data.sum(axis=1).sort_values(ascending=False).reset_index()
    total_wins.columns = ['name', 'Total Wins']  # Renaming for clarity
    # Merge total wins with pokemon_data on the Pokémon name
    merged_data = pd.merge(pokemon_data.reset_index(), total_wins, on='name')
    col_drop, empty_col,col_image = st.columns([5,1,2])
    selected_pokemon = col_drop.selectbox('Select a Pokémon:', options=battle_data.columns, key='pokemon_select_2')
    col_image.image(pokemon_data.loc[selected_pokemon, 'image_url'], width=100)  # Smaller width
    plot_performance(selected_pokemon)

# Page 3: Selected Pokémon Stats
with page3:
    st.title('Pokémon Stat Comparison')
    # Calculate total wins for each Pokémon
    battle_data_key = st.selectbox('Select a win data file:', options=file_options_wins, key='file_select3')  # Dropdown menu for file selection
    st.write("---")  # Add a separator
    battle_data = load_data(file_options_wins[battle_data_key], index_col='name')
    total_wins = battle_data.sum(axis=1).sort_values(ascending=False).reset_index()
    total_wins.columns = ['name', 'Total Wins']  # Renaming for clarity
    # Merge total wins with pokemon_data on the Pokémon name
    merged_data = pd.merge(pokemon_data.reset_index(), total_wins, on='name')
    # Create two columns
    col1, col2 = st.columns(2)
    # Selection boxes for choosing Pokémon to compare
    pokemon1 = col1.selectbox('Select a Pokémon:', options=pokemon_data.index, key='pokemon1_select_3')
    pokemon2 = col2.selectbox('Select the opponent Pokémon:', options=pokemon_data.index, key='pokemon2_select_3')
    # Get color for each Pokémon
    pokemon1_color, pokemon2_color = get_pokemon_color(pokemon_data.loc[pokemon1, 'type1'], pokemon_data.loc[pokemon1, 'type2'], pokemon_data.loc[pokemon2, 'type1'], pokemon_data.loc[pokemon2, 'type2'])
    # Adjust the ratios to give more space to the middle column and less to the side columns
    col1, col_plot, col2 = st.columns([1, 4, 1])
    # 1st Pokemon card
    display_pokemon_details(col1, pokemon1)
    # display pokemon stats 
    max_base_total = pokemon_data['base_total'].max() + 50
    compare_pokemon(col_plot, pokemon1, pokemon2, pokemon1_color, pokemon2_color, max_base_total)
    # 2nd Pokemon card
    display_pokemon_details(col2, pokemon2)
    moves = pd.concat((move_data.loc[move_data['name'].isin([pokemon1])], (move_data.loc[move_data['name'].isin([pokemon2])]))).set_index('move').drop(columns=['name','level', 'gen']).drop_duplicates()
    col1, col_df, col2 = st.columns([1, 20, 1])
    col_df.write(moves)
    
    st.write("---")  # Add a separator
    
    # Use columns to create a visual effect of right-justified "Losses"
    col_space, col_wins, col_draws, col_losses = st.columns([1, 2, 2, 2])

    wins = battle_data.loc[pokemon1, pokemon2]
    losses = battle_data.loc[pokemon2, pokemon1]
    if 'Level 50' in battle_data_key:
        draws = 100 - wins - losses
    else:
        draws = 1000 - wins - losses
    with col_wins:
        # Display Wins
        st.metric(label="Wins", value=wins)
    with col_draws:
        # Display Wins
        st.metric(label="Draws", value=draws)
    with col_losses:
        # Display Losses
        st.metric(label="Losses", value=losses)
    
    st.write("---")  # Add a separator for visual clarity

    # Button for initiating the battle
    if st.button('Battle!'):
        # Temporarily redirect stdout to capture the prints from the runbattle function
        f = io.StringIO()
        with redirect_stdout(f):
            pk.runbattle(pk_dict[pokemon1], pk_dict[pokemon2], verbose=True)
        output = f.getvalue()
        
        # Display the captured output in the Streamlit app
        st.text_area("Battle Output", output, height=300)
    
    st.write("---")  # Add a separator
    st.title('Health Remaining Comparison')
    # Add page description
    with st.expander("Description"):
        st.markdown("""
                    This page is for visualizing the health stats of two Pokémon after 100 battles. 
                    The histogram below shows the distribution of remaining health percentages for each 
                    Pokémon after 100 battles. The data is based on the selected health data file. Furthermore,
                    the count of 0s is filtered out to provide a clearer view of the data as 0s represent battles
                    where the Pokémon fainted.
                    """)
    # Selection box for health data
    health_data_key = st.selectbox('Select a health data file:', options=file_options_health, key='health_data_select')
    health_data = load_data(file_options_health[health_data_key])
    # Convert column names to tuples
    column_mapping = {column: ast.literal_eval(column) for column in health_data.columns}
    health_data.rename(columns=column_mapping, inplace=True)
    health_data.columns = ['_'.join(col) for col in health_data.columns.values]
    st.write("---")  # Add a separator for visual clarity
    # create tuple of pokemon names
    pokemon_pair = pokemon1 + '_' + pokemon2
    # get the heals data for the pair
    health_pair = health_data[pokemon_pair]
    # filter out the 0s
    health_pair = health_pair[health_pair > 0]  
    # Adjust the ratios to give more space to the middle column and less to the side columns
    col1, col_plot, col2 = st.columns([1, 6, 1])
    for i in range(10):
        col1.write(' ')
    col1.image(pokemon_data.loc[pokemon1, 'image_url'], width=100)  # Smaller width
    # plot histogram of heals
    with col_plot:
        fig = px.histogram(health_pair, nbins=10, title=f'{pokemon1} vs {pokemon2} Health Remaining After 100 Battles')
        fig.update_xaxes(title_text=f"{pokemon1}'s remaining health (%)", range=[0.1, 1])  # Set horizontal axis range
        fig.update_layout(showlegend=False)  # Hide legend
        fig.update_traces(marker_color=pokemon1_color)  # Set marker color
        st.plotly_chart(fig, use_container_width=True)
    for i in range(10):
        col2.write(' ')
    col2.image(pokemon_data.loc[pokemon2, 'image_url'], width=100)  # Smaller width
    st.write("---")  # Add a separator for visual clarity

    st.title('Battle Length Comparison')
    # Add page description
    with st.expander("Description"):
        st.markdown("""
                    This page is for visualizing the number of turns taken between two Pokémon after 100 battles. 
                    The histogram below shows the distribution of turns where the data is based on the selected time data file.
                    """)
    # Selection box for time data
    time_data_key = st.selectbox('Select a time data file:', options=file_options_times, key='time_data_select')
    time_data = load_data(file_options_times[time_data_key])
    # Convert column names to tuples
    column_mapping = {column: ast.literal_eval(column) for column in time_data.columns}
    time_data.rename(columns=column_mapping, inplace=True)
    time_data.columns = ['_'.join(col) for col in time_data.columns.values]
    st.write("---")  # Add a separator for visual clarity
    # get the time data for the pair
    time_pair = time_data[pokemon_pair]
    # Adjust the ratios to give more space to the middle column and less to the side columns
    col1, col_plot, col2 = st.columns([1, 6, 1])
    # 1st Pokemon image
    for i in range(10):
        col1.write(' ')
    col1.image(pokemon_data.loc[pokemon1, 'image_url'], width=100)  # Smaller width
    # plot histogram of time
    with col_plot:
        fig = px.histogram(time_pair, nbins=10, title=f'{pokemon1} vs {pokemon2} Time Taken After 100 Battles')
        fig.update_xaxes(title_text=f"{pokemon1}'s time taken (s)")  # Set horizontal axis range
        fig.update_layout(showlegend=False)
        fig.update_traces(marker_color=pokemon1_color)
        st.plotly_chart(fig, use_container_width=True)
    # 2nd Pokemon image
    for i in range(10):
        col2.write(' ')
    col2.image(pokemon_data.loc[pokemon2, 'image_url'], width=100)  # Smaller width
    
# Page 4: Team Battle Data
with page4:
    st.title('Team Battle Performance')
    # Add page description
    with st.expander("Page Description"):
        st.markdown("""
                    This page is for visualizing the performance of our chosen teams of pokémon.
                    Each team faces the Elite Four and their performance is recorded in the data files.
                    """)

    st.write("---")  # Add a separator for visual clarity
    
    total_wins, avg_times, enemy_dict = all_teams_results(team_data)
    efficiences = [wins/time if time > 0 else 0 for wins, time in zip(total_wins, avg_times)]
    plot_battle_wins(total_wins, team_data, list(teams_dict.values()))
    
    st.write("---")  # Add a separator for visual clarity
    
    plot_battle_times(avg_times, total_wins, team_data, list(teams_dict.values()))

    st.write("---")  # Add a separator for visual clarity

    # Allow user to select an attribute to compare against Total Wins
    attribute_options = ['base_total', 'hp', 'speed', 'attack', 'defense', 'sp_attack', 'sp_defense'] 
    metric_options = ['Total Wins', 'Average Time', 'Efficiency: (Wins/avg_Time)']
    selected_attribute = st.selectbox("Select an attribute to compare:", options=attribute_options, key='attribute_select_4')
    selected_metric = st.selectbox("Select a metric to compare:", options=metric_options, key='metric_select_4')
    merged_data2 = pd.DataFrame({'Team': team_stat_df.index, 'Total Wins': total_wins, 'Average Time': avg_times, 'Efficiency: (Wins/avg_Time)': efficiences})
    merged_data2 = pd.merge(merged_data2, team_stat_df, left_on='Team', right_index=True)
    plot_team_wins_vs_attribute(merged_data2, selected_attribute, selected_metric)
    
    st.write("---")  # Add a separator for visual clarity
    team_data_value = st.selectbox('Select a team:', options=teams_dict.values(), key='team_data_select')
    team_data_key = list(teams_dict.keys())[list(teams_dict.values()).index(team_data_value)]
    team = (team_data[team_data_key]).copy()
    wins, times, enemy_dict = get_total_wins_and_times(team)
    st.write("---")  # Add a separator for visual clarity
    
    # Use columns to create a visual effect of right-justified "Losses"
    colspace, col_wins, col_losses = st.columns([1, 2, 2])
    with col_wins:
        # Display Wins
        st.metric(label="Elite Four Victories", value=wins)
    with col_losses:
        # Display Losses
        st.metric(label="Elite Four Defeats", value=1000 - wins)
    st.write("---")  # Add a separator for visual clarity

    # display team stats
    col1, colplot, col2 = st.columns([1, 4, 1])
    max_base_total = 0
    for i in range(len(team_data_value)):
        max_base_total += pokemon_data.loc[team_data_value[i], 'base_total']
    max_base_total = max_base_total + max_base_total/10
    elite4_member = st.selectbox('Select an Elite Four Team to compare against:', options=elite_dict, key='team2_data_select')
    elite4_team = elite_dict[elite4_member]
    st.write(f'{elite4_team}')
    team1_color, team2_color = get_pokemon_color(pokemon_data.loc[team_data_value[0], 'type1'], pokemon_data.loc[team_data_value[0], 'type2'], pokemon_data.loc[elite4_team[1], 'type1'], pokemon_data.loc[elite4_team[1], 'type2'])
    compare_teams(colplot, team_data_value, elite4_team, team1_color, team2_color, max_base_total)
   
    col2.subheader(elite4_member)
    col2.image(elite_four_images[elite4_member], width=100)  # Smaller width

    st.write("---")  # Add a separator for visual clarity
    # Display a table of enemy_dict
    st.write("Losses to Elite Four Members:")
    # Convert dictionary to DataFrame with keys as indexes
    df = pd.DataFrame.from_dict(enemy_dict, orient='index', columns=['Defeats'])
    # transpose dataframe
    df = df.T
    # Sort by 'Defeats' and display as a Markdown table
    st.markdown(df.to_markdown())
    st.write("---")  # Add a separator for visual clarity
    
    plot_times(times, team_data_key)
    

# Page 5: Pick a Team
with page5:
    st.title('Pick a Team')
    # Add page description
    with st.expander("Page Description"):
        st.markdown("""
                    This page is for selecting a team of pokémon to battle the Elite Four. 
                    The performance of the team will be recorded and displayed in the Team Battle Data page.
                    """)
    col1, col2, col3 = st.columns(3)
    # Create a selection box for choosing a team
    member_1 = col1.selectbox('Select your 1st Pokémon:', options=pokemon_data.index, key='pokemon1_select_7')
    member_2 = col2.selectbox('Select your 2nd Pokémon:', options=pokemon_data.index, key='pokemon2_select_7')
    member_3 = col3.selectbox('Select your 3rd Pokémon:', options=pokemon_data.index, key='pokemon3_select_7')
    member_4 = col1.selectbox('Select your 4th Pokémon:', options=pokemon_data.index, key='pokemon4_select_7')
    member_5 = col2.selectbox('Select your 5th Pokémon:', options=pokemon_data.index, key='pokemon5_select_7')
    member_6 = col3.selectbox('Select your 6th Pokémon:', options=pokemon_data.index, key='pokemon6_select_7')
    team = [member_1, member_2, member_3, member_4, member_5, member_6]
    # Display the team members with their sprites
    st.write("Team Members:")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    for i in range(6):
        display_pokemon_details(eval(f'col{i+1}'), team[i])
    st.write("---")  # Add a separator for visual clarity
    myteam = pk.create_pokemon_objects(team)
    # Button for initiating the battle
    if st.button('Battle the Elite Four!'):
        f = io.StringIO()
        with redirect_stdout(f):
            myresult,mytime,winner,winnerlist = pk.run_elite(myteam,elite,verbose=True,roundreset=False)
        output = f.getvalue()
        if myresult == 1:
            st.write(f'Congratulations! You have defeated the Elite Four! It only took {mytime*10:.0f} turns.')
        else:
            st.write(f"You have been defeated by {winner}'s {winnerlist[-1]}!")
        # Display the captured output in the Streamlit app
        st.text_area("Battle Output", output, height=300)
        