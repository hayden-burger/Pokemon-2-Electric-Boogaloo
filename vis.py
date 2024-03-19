"""
This script is created by Hayden Burger, Corinne Desroches, David Lee, and John Tyler 
with additional assistance provided through ChatGPT.

Description:
    This script builds a streamlit dashboard to visualize the results of 
    generation 1 pokemon battles. Every pokemon battles every other pokemon
    and the win tally is recorded in a dataframe which is exported to 1000runs.csv.
    The pokemon stats and win tallys are compared and visualized.
"""
# import statements
import streamlit as st
import pandas as pd
import plotly.express as px
# import plotly.graph_objects as go   # Used for plotting scatterplot with sprites
import pokemon_module as pk
import numpy as np
import io
from contextlib import redirect_stdout

# Load the data
@st.cache_data  # Corrected decorator for caching data
def load_data(filepath, **kwargs):
    if filepath.endswith('.xlsx'):
        return pd.read_excel(filepath, **kwargs)
    elif filepath.endswith('.csv'):
        return pd.read_csv(filepath, **kwargs)
    else:
        raise ValueError("Unsupported file format. Please use a CSV or XLSX file.")

# Adjust the path to your file
battle_data_path = '1000runs.csv'
battle_data = load_data(battle_data_path, index_col='name')
pokemon_data = pk.Pokemon_df
move_data = pk.merged_moves_df

# Calculate total wins for each Pokémon
total_wins = battle_data.sum(axis=1).sort_values(ascending=False).reset_index()
total_wins.columns = ['name', 'Total Wins']  # Renaming for clarity
# Merge total wins with pokemon_data on the Pokémon name
merged_data = pd.merge(pokemon_data.reset_index(), total_wins, on='name')

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
def plot_total_wins(tab, battle_data):
    fig_total_wins = px.bar(total_wins, x='name', y='Total Wins',
                            title='Total Wins per Pokémon')
    fig_total_wins.update_layout(xaxis_title='Pokémon', yaxis_title='Number of Wins')
    tab.plotly_chart(fig_total_wins)
    
    
# Function to plot a scatterplot of Pokémon base_total
def plot_total_wins_vs_attribute(merged_data, attribute):
    fig_scatter = px.scatter(merged_data, x='Total Wins', y=attribute, text='name',
                     title=f"Pokémon Total Wins vs. {attribute.capitalize()}", 
                     hover_data=['type1', 'type2'])
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.update_layout(height=600, xaxis_title='Total Wins', yaxis_title=attribute.capitalize())
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
def plot_performance(tab, selected_pokemon):
    performance_data = battle_data.loc[selected_pokemon,:].copy()
    performance_data = performance_data.sort_values(ascending=False)
    
    fig_performance = px.bar(performance_data, y=performance_data.values,
                                title=f'Performance Scores for {selected_pokemon}')
    fig_performance.update_layout(xaxis_title='Opponent', yaxis_title='Number of Wins')
    tab.plotly_chart(fig_performance)

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
                    Wt: {details['weight_kg']} kg<br>
                    Moves: {', '.join(moves.values)}
                    """
    # Display details in the specified column
    with column:
        st.markdown(html_content, unsafe_allow_html=True)

# Comparison function with color coding integration
def compare_pokemon(column, pokemon1, pokemon2, pokemon1_color, pokemon2_color):
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

# Streamlit app layout
st.title('Pokémon Battle Performance')

# Create tabs
tab1, tab2, tab3 = st.tabs(["Total Wins", "Selected Pokémon Performance", "Selected Pokémon Stats"])

# Tab 1: overall performance bar graph and scatter plot on attributes
with tab1:
    #Add App description
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

    plot_total_wins(tab1, battle_data)
    
    st.write("---")  # Adds a visual separator

    # Allow user to select an attribute to compare against Total Wins
    attribute_options = ['type1', 'type2', 'base_total', 'hp', 'speed', 'attack', 'defense', 'sp_attack', 'sp_defense'] # Assuming 'name' is not in pokemon_data columns
    selected_attribute = st.selectbox("Select an attribute to compare with Total Wins:", options=attribute_options, key='attribute_select_tab1')
    plot_total_wins_vs_attribute(merged_data, selected_attribute)

# Tab 2: Dropdown menu for selecting a Pokémon and plotting its performance
with tab2:
    col_drop, empty_col,col_image = st.columns([5,1,2])
    selected_pokemon = col_drop.selectbox('Select a Pokémon:', options=battle_data.columns, key='pokemon_select_tab2')
    col_image.image(pokemon_data.loc[selected_pokemon, 'image_url'], width=100)  # Smaller width
    plot_performance(tab2, selected_pokemon)

# Tab 3: User picks two pokemon to compare side by side with an option to simulate a battle live
with tab3:
    # Selection boxes for choosing Pokémon to compare
    pokemon1 = st.selectbox('Select a Pokémon:', options=pokemon_data.index, key='pokemon1_select_tab3')
    pokemon2 = st.selectbox('Select the opponent Pokémon:', options=pokemon_data.index, key='pokemon2_select_tab3')
    # Get color for each Pokémon
    pokemon1_color, pokemon2_color = get_pokemon_color(pokemon_data.loc[pokemon1, 'type1'], pokemon_data.loc[pokemon1, 'type2'], pokemon_data.loc[pokemon2, 'type1'], pokemon_data.loc[pokemon2, 'type2'])
    # Adjust the ratios to give more space to the middle column and less to the side columns
    col1, col_plot, col2 = st.columns([1, 4, 1])
    # 1st Pokemon card
    display_pokemon_details(col1, pokemon1)
    # display pokemon stats 
    max_base_total = pokemon_data['base_total'].max() + 50
    compare_pokemon(col_plot, pokemon1, pokemon2, pokemon1_color, pokemon2_color)
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
        pk_dict = assign_pokemon_class()
        # Temporarily redirect stdout to capture the prints from the runbattle function
        f = io.StringIO()
        with redirect_stdout(f):
            pk.runbattle(pk_dict[pokemon1], pk_dict[pokemon2], verbose=True)
        output = f.getvalue()
        
        # Display the captured output in the Streamlit app
        st.text_area("Battle Output", output, height=300)