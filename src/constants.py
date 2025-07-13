"""Constants and configuration for the Solar System simulation."""

# Screen dimensions (1920x1080 for better visibility of outer planets)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
ORBIT_COLOR = (50, 50, 50)  # Dark gray for orbit paths

# Scale factors for visualization
DISTANCE_SCALE = 30  # pixels per AU

# Time step (in Earth days)
TIME_STEP = 1.0

# Astronomical Unit in km
AU = 149.6e6  # 1 AU = 149.6 million km

# Gravitational constant (km^3 kg^-1 s^-2)
G = 6.67430e-20

# Celestial body data (semi-major axis in AU, orbital period in Earth days, radius in km, color)
CELESTIAL_BODIES = {
    'Sun': {'radius': 696340, 'color': YELLOW, 'mass': 1.989e30},
    'Mercury': {'semi_major_axis': 0.39, 'orbital_period': 88, 'radius': 2439.7, 'color': GRAY, 'mass': 3.3011e23},
    'Venus': {'semi_major_axis': 0.72, 'orbital_period': 224.7, 'radius': 6051.8, 'color': (255, 165, 0), 'mass': 4.8675e24},
    'Earth': {'semi_major_axis': 1.0, 'orbital_period': 365.25, 'radius': 6371, 'color': BLUE, 'mass': 5.972e24},
    'Mars': {'semi_major_axis': 1.52, 'orbital_period': 687, 'radius': 3389.5, 'color': RED, 'mass': 6.417e23},
    'Jupiter': {'semi_major_axis': 5.2, 'orbital_period': 4332.59, 'radius': 69911, 'color': (255, 215, 0), 'mass': 1.898e27},
    'Saturn': {'semi_major_axis': 9.58, 'orbital_period': 10759.22, 'radius': 58232, 'color': (210, 180, 140), 'mass': 5.683e26},
    'Uranus': {'semi_major_axis': 19.22, 'orbital_period': 30688.5, 'radius': 25362, 'color': (173, 216, 230), 'mass': 8.681e25},
    'Neptune': {'semi_major_axis': 30.05, 'orbital_period': 60182, 'radius': 24622, 'color': (0, 0, 139), 'mass': 1.024e26}
}
