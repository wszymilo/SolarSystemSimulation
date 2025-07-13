# Solar System Simulation

A Python simulation of our Solar System using Pygame, featuring accurate 
relative sizes and orbital speeds of planets. Size of the Sun is reduced to make
the inner planets visible.

## Features

- Realistic relative sizes of planets
- Accurate orbital periods
- Adjustable simulation speed
- Pause/Resume functionality
- Clean, informative UI

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Simulation

```bash
python -m src.main
```

## Controls

- **SPACE**: Pause/Resume the simulation
- **UP ARROW**: Increase simulation speed
- **DOWN ARROW**: Decrease simulation speed
- **ESC**: Quit the simulation

## Project Structure

- `src/`: Source code
  - `celestial_body.py`: Base class for all celestial bodies
  - `solar_system.py`: Main simulation class
  - `constants.py`: Configuration and constants
  - `main.py`: Entry point
- `test/`: Unit tests
- `requirements.txt`: Project dependencies

## Testing

To run the tests with coverage:

```bash
pytest --cov=src test/
```

## Dependencies

- Python 3.7+
- Pygame 2.5.2+
- Pytest (for testing)
