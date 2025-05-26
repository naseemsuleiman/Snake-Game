# Snake Game

A classic Snake game implemented in Python using Pygame. This project lets you control a snake, eat apples to grow longer, and try to survive as long as possible without hitting walls or your own tail. The game features multiple difficulty levels, a graphical interface, sound effects, and high score tracking.

## Features

- **Classic Gameplay:** Control the snake with arrow keys, eat apples to grow, and avoid crashing into walls or yourself.
- **Difficulty Levels:** Choose from Easy, Medium, or Hard for different game speeds.
- **High Scores:** Tracks high scores for each difficulty level.
- **Graphics and Sounds:** Custom graphics for the snake, apple, and game board, plus sound effects for eating apples.
- **User Interface:** Buttons for starting the game, viewing high scores, restarting, quitting, and viewing instructions.
- **Instructions Modal:** In-game help explains controls and gameplay basics.

## How to Play

- Use the **arrow keys** to move the snake in four directions.
- **Eat apples** to grow longer and increase your score.
- **Avoid walls and your own tail**—colliding with either will end the game.
- The game speeds up as you pick higher difficulties.
- Select your preferred difficulty before starting the game.

### Controls

- **Arrow Keys:** Move the snake (Up, Down, Left, Right)
- **Start Game:** Begin a new game session
- **Restart:** Restart the current game after a game over
- **Quit:** Exit the game
- **How to Play:** View the instructions modal
- **High Scores:** View the leaderboard for each difficulty

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/naseemsuleiman/Snake-Game.git
   cd Snake-Game
   ```

2. **Install dependencies:**
   - Make sure you have Python 3.x installed.
   - Install Pygame:
     ```bash
     pip install pygame
     ```

3. **Run the game:**
   ```bash
   python app.py
   ```

## Assets

- Place all graphics in the `Graphics/` directory (e.g., `head_up.png`, `apple.png`, etc.).
- Place the font file in the `Font/` directory (e.g., `PoetsenOne-Regular.ttf`).
- Place the sound file in the `Sound/` directory (e.g., `Sound_crunch.wav`).

The game will not start if the required assets are missing.

## Project Structure

```
Snake-Game/
├── app.py
├── Graphics/
│   ├── head_up.png
│   ├── tail_left.png
│   └── ... (other graphics)
├── Font/
│   └── PoetsenOne-Regular.ttf
├── Sound/
│   └── Sound_crunch.wav
└── README.md
```

## Customization

- Add more graphics or sounds by placing them in the correct directories and modifying `app.py` as needed.
- Adjust speeds or scoring by changing values in `app.py`.

## License

This project is open-source and available under the MIT License.

---

Enjoy playing Snake!
