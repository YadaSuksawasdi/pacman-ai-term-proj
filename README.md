# AI Game Project: Two-Player Coin Collection Game

## Project Overview

This repository contains the implementation of a two-player coin collection game, developed as part of the Artificial Intelligence course at International School of Engineering, Chulalongkorn University. The project demonstrates the application of various AI techniques, focusing on agent reasoning and interaction in a competitive scenario.

## Game Description

The game is played on an 8x8 board where two AI agents compete to collect coins. Key features include:

- Players start in opposite corners of the board
- Coins are randomly placed on the board at the start of the game
- Players take turns moving one cell at a time (up, down, left, or right)
- Collecting a coin increases a player's score
- Coins have a 50% chance of becoming "transparent" each turn, making them uncollectible
- Transparent coins have a 50% chance of becoming solid again each turn
- Players receive bonus points for collecting consecutive coins
- The game ends when no collectable coins remain

## AI Implementation

The AI for both players is implemented using the following techniques:

1. **State Representation**: Each game state includes the coin map, remaining coins, player scores, and consecutive coin streaks.

2. **Movement**: Players can move in four directions within the board boundaries.

3. **Fitness Function**: Calculates the best possible moves by recursively evaluating future rounds and coin probabilities.

4. **Genetic Algorithm**: Used to determine optimal move sequences for each player.

5. **Probabilistic Reasoning**: Accounts for the non-deterministic nature of coin states.

## Code Structure

The main components of the code include:

- `State` class: Represents the game state and handles moves
- `fitness` function: Evaluates the quality of potential moves
- `ga` function: Implements the genetic algorithm for path finding
- `coin_update` function: Manages the random state changes of coins
- Main game loop: Alternates turns between players and updates the game state

## Running the Game

To run the game, you need:

Python installed on your system
The random library (which is part of Python's standard library)

To start the game:

Download the Python file containing the game code
Open a terminal or command prompt
Navigate to the directory containing the file
Run the command: python filename.py (replace 'filename.py' with the actual name of the file)

The game will automatically run until a winner is determined.

## Future Improvements

For future development, the following enhancements are planned:

1. **Player Interaction**: Modify the game to allow a human player to compete against the AI. This will make the game more interactive and help in better understanding the algorithm and code.
2. **User Interface**: Develop a graphical user interface for a more engaging user experience.
3. **Performance Optimization**: Improve the efficiency of the AI algorithms for faster gameplay.
4. **Difficulty Levels**: Implement different levels of AI difficulty for varied gameplay experiences.

## Contributors

6438053221 Yada Suksawasdi
For any suggestions, recommendations, or discussions about this project, please feel free to contact me at kun9k1n9@gmail.com

## Acknowledgments

This project was developed as part of the 2147332 Artificial Intelligence course at International School of Engineering, Chulalongkorn University, under the guidance of Prof. Paulo Garcia.
