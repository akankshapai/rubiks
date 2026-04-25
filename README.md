🧩 Rubik's Cube Solver & 3D Visualizer

A complete Rubik’s Cube project featuring an algorithmic solver, an interactive 3D graphical interface, and an automated testing suite.



🚀 Features

* 3D Visualization
* Built with the Ursina engine for a smooth and interactive cube experience.
* Algorithmic Solver
* Uses a state-preserving Layer-by-Layer (Beginner’s Method) approach.
* Dynamic Controls
* Rotate faces manually using the keyboard with real-time move tracking.
* Sound Effects
* Includes a fun feature: each manual turn triggers a playful "meow" sound effect.
* Move Simplification
* Automatically optimizes move sequences, such as simplifying R R R into R'.
* Command Line Interface
* Lightweight text-based cube interaction via terminal.
* Automated Test Suite
* Extensive randomized scramble testing to validate solver reliability.



🛠️ Installation

Prerequisites:

* Python 3.10+
* Ursina Engine

Setup

```git clone https://github.com/akankshapai/rubiks.git```

```cd rubics```

```pip install ursina```



🎮 Usage

3D Mode (Recommended)

Run the graphical interface:

```python graphics.py```

Controls:

* Rotate face → R, L, U, D, F, B
* Inverse rotation → Shift + key
* Scramble → S
* Reset → T
* Quit → Q
* Auto Solve → Click AUTO SOLVE



Command Line Mode

```python cube_main.py```



📂 Project Structure

* graphics.py — 3D interface entry point
* solver.py — solving logic and move optimization
* moves.py — cube mechanics and transformations
* tests/ — automated testing scripts
* sounds/ — audio assets



🧪 Testing

Run the test suite:

```python -m tests.test_solver```

Tests include randomized scrambles to ensure consistent solving performance.



🤓 Fun Fact: The “Sexy Move”

The sequence R U R' U' is one of the most commonly used patterns in beginner cube-solving methods.



📌 Notes

* This project focuses on making things clear and correct, rather than trying to do them quickly.
* Great for understanding what's going on behind the scenes with cube-solving algorithms.


👥 Authors

- [Ashwin Bhat K](https://github.com/ashwinbhatk)
- [Akanksha Ashwin Pai](https://github.com/akankshapai)
