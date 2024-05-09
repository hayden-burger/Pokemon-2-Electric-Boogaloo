# Pokémon 2 Electric Boogaloo - Hayden Burger Branch

Our team meets again, but this time with a larger scope for our project. Our goal: what 6-Pokémon team can most efficiently beat the Elite Four

## About This Repository

This repository includes data source files in CSV format, Python modules, and a Jupyter notebook that collectively run the battle simulations. The core functionality is encapsulated within `pokemon_module.py`, which defines the Pokémon classes, battle mechanics, and simulation logic. An example of our orignal project can be accessed via a Streamlit app, accessible [here](https://pokemonnearpeerbattlesim3801.streamlit.app/), visualizes the simulation outcomes.

### Contributors

- Hayden Burger
- Corinne Desroches
- David Lee

Special thanks to our course instructors and peers at NPS for their support and guidance throughout this project.

### Data Files

- **`1000runs.csv`**: Contains the outcomes of 1,000 simulated battles for each Pokémon pairing.
- **`Pokemon.csv`**: Provides the base stats, available moves, and other attributes for each Generation 1 Pokémon.
- **`Move_set_per_pokemon.csv`**: Details the moves available to each Pokémon and their effects.
- **`Moveset.csv`**: Details the moves with their type, power, accuracy, effects, and effect probability.
- **`Requirements.txt`**: Lists the packages needed for the Streamlit app.

### Python Files

- **`Pokemon_module.py`**: Contains the data cleaning and resulting dataframes, the Pokémon class, and the battle functions.
- **`Vis.py`**: Contains the script to visualize the `1000runs.csv` file in a Streamlit App.
- **`Jupyter Notebook`**: Jupyter Notebook to perform 1000 iterations of every pokemon battle and exported to csv. Also contains functions and code to build visuals.

### Project Overview

Our project applies Python programming and data visualization skills to simulate and analyze battles between all 151 Generation 1 Pokémon, each battling every other Pokémon 1,000 times. This required:

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
