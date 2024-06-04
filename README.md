# Pokémon 2 Electric Boogaloo

Our team meets again, but this time with a larger scope for our project. Our goal: what 6-Pokémon team can most efficiently beat the Elite Four

## About This Repository

### Contributors

- Hayden Burger
- Corinne Desroches
- David Lee

Special thanks to our course instructors and peers at NPS for their support and guidance throughout this project.

### Distribution Exploration

These files were used for developing distributions that would have been put into a Simio Model. We ended up scrapping that idea due to time constraints; however, this is included in the REPO to supplement our presentation and paper.

- **`DistributionTesting.py`**: Tests for determining best distribution fits for any data.
- **`pokemon_distributions`**: Used to develop distributions for our data.

### Input Data Files

- **`Move_set_per_pokemon.csv`**: Details the moves available to each Pokémon and their effects.
- **`Moveset.csv`**: Details the moves with their type, power, accuracy, effects, and effect probability.
- **`Pokemon Teams.xlsx`**: Details the composition of each team chosen and a description.
- **`Pokemon.csv`**: Provides the base stats, available moves, and other attributes for each Generation 1 Pokémon.

### Output Data Files

- **`100runs_______.csv`**: These were made from battling each pokemon against each other 100 times - used for Distribution Exploration.
- **`Level_1_1000runs.csv`**: These were the results from the first project of battling all Pokemon 1000 times.
- **`Random_Team_Summary.csv`**: Details the results from randomly generated teams battling the Elite Four.
- **`elite_results.csv`**: Details the results from **`Pokemon Teams.xlsx`** battling the Elite Four.

### Presentation and Paper

Contains the presentationa and paper submitted for our final project.

### Python Files

- **`Pokemon_module.py`**: Contains the data cleaning and resulting dataframes, the Pokémon class, and the battle functions.
- **`Vis.py`**: Contains the script to visualize the results in a Streamlit App.
- **`Requirements.txt`**: Lists the packages needed for the Streamlit app.
- **`testpokemon.ipynb`**: Jupyter Notebook used to explore our project. Also contains functions and code to build visuals.

### Project Overview

Our project applies Python programming and data visualization skills to simulate and analyze battles between teams of 6 pokemon vs the generation one Elite Four. This required:

- Parsing CSV files for Pokémon stats and move sets.
- Developing a Python class to represent Pokémon, including attributes for stats and moves.
- Implementing battle logic with methods for selecting moves, applying effects, and calculating damage.
- Simulating battles and capturing outcomes for analysis.
- Visualizing results with Plotly and Streamlit.

### Getting Started

1. **Clone this repository**: Get a local copy for exploration and experimentation.
2. **Explore the directories**: Each contains unique aspects of the project, with detailed `README.md` files.
3. **Run the Jupyter notebook and Streamlit app**: Dive into the code and visualizations.

### Prerequisites

- Python 3.x installed.
- Familiarity with Python programming.
- Optionally, an IDE like PyCharm or VS Code for a better development experience.

### Contributing

Contributions, suggestions, and feedback are welcome! Feel free to fork the repository, create a feature branch, and submit pull requests with improvements or new content.

### Contact

Questions or discussions? Reach out via our NPS email addresses.

### Acknowledgements

Our heartfelt thanks to the NPS faculty and our classmates for their invaluable input and encouragement throughout this project.
