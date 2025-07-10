# Connect 4 AI Game

This project implements a Connect 4 game where you can play against an AI opponent. The AI uses the Minimax algorithm with alpha-beta pruning to make optimal moves, ensuring it wins every time when it starts as the first player.

## Features

- Play Connect 4 against an AI opponent
- AI uses Minimax algorithm with alpha-beta pruning for optimal decision making
- AI race mode where multiple AI agents can play against each other
- Configurable game depth for the AI

## Algorithm

The AI agent uses the Minimax algorithm with alpha-beta pruning to decide the best move. This algorithm is a recursive algorithm used for decision-making in game theory, providing an optimal move for the player assuming that the opponent is also playing optimally.

### Heuristic Function

The heuristic function evaluates the game state and assigns a score based on:

- Center column control (higher weight as it provides more opportunities)
- Horizontal, vertical, and diagonal connections (evaluating potential connections of 2, 3, and 4 pieces)
- Blocking opponent's moves (assigning negative scores to positions that could lead to the opponent's win)

## Experiments and Performance

We conducted several experiments to evaluate the performance of the AI agent by varying the depth of the Minimax algorithm:

- **Depth 3 and below**: The AI performed poorly, often making suboptimal moves
- **Depth 5**: Significant improvement with more strategic moves
- **Depth 6**: Balanced offensive and defensive strategies
- **Depth 7 and above**: Became overly cautious, focusing too much on not losing

The optimal depth for the Minimax algorithm lies between 4 and 7.

## AI Race

The `ai_race.py` file allows multiple AI agents to play against each other. This can be used to evaluate different AI strategies and configurations.

## Pre-requirements

- Python 3.x
- uv (Python package installer and resolver)

## Installation

1. Clone the repository
2. Use `uv` to install dependencies automatically
3. Run `uv run main.py` to play against the AI
4. Run `uv run ai_race.py` to make AIs race each other

## How to Play

1. Run the main game file to start a game against the AI
2. Make your moves by selecting columns
3. The AI will automatically make its move after yours

## Future Improvements

- Implementing a more sophisticated heuristic function
- Using machine learning techniques to dynamically adjust the depth
- Incorporating Monte Carlo Tree Search (MCTS) for better move exploration
