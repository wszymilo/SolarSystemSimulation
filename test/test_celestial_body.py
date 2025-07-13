"""Tests for the CelestialBody class."""
import math

from src.celestial_body import CelestialBody
from src.constants import CELESTIAL_BODIES, DISTANCE_SCALE


def test_celestial_body_initialization():
    """Test that a celestial body is initialized correctly."""
    # Test data for Earth
    earth_data = CELESTIAL_BODIES['Earth']
    earth = CelestialBody(
        name='Earth',
        radius=earth_data['radius'],
        color=earth_data['color'],
        mass=earth_data['mass'],
        semi_major_axis=earth_data['semi_major_axis'],
        orbital_period=earth_data['orbital_period']
    )
    
    # Verify attributes
    assert earth.name == 'Earth'
    assert earth.radius == earth_data['radius']
    assert earth.color == earth_data['color']
    assert earth.mass == earth_data['mass']
    assert earth.semi_major_axis == earth_data['semi_major_axis']
    assert earth.orbital_period == earth_data['orbital_period']
    
    # Verify position is initialized (should be at semi-major axis + center)
    expected_x = earth.semi_major_axis * DISTANCE_SCALE + 960  # 960 is CENTER_X (1920/2)
    expected_y = 500
    
    assert abs(earth.x - expected_x) < 1e-6
    assert abs(earth.y - expected_y) < 1e-6
    
    # Verify angle and angular velocity are initialized correctly
    assert earth.angle == 0
    assert abs(earth.angular_velocity - (2 * math.pi / earth.orbital_period)) < 1e-6


def test_sun_initialization():
    """Test that the Sun is initialized correctly."""
    sun_data = CELESTIAL_BODIES['Sun']
    sun = CelestialBody(
        name='Sun',
        radius=sun_data['radius'],
        color=sun_data['color'],
        mass=sun_data['mass']
    )
    
    # Sun should have no orbital parameters
    assert sun.semi_major_axis == 0
    assert sun.orbital_period == 0
    
    # Velocity should be zero for the Sun (it's the center of the system in this simulation)
    assert sun.vx == 0
    assert sun.vy == 0


def test_update_position():
    """Test that updating position works correctly."""
    # Create a test planet with a 100-day orbital period
    test_planet = CelestialBody(
        name='TestPlanet',
        radius=1000,
        color=(255, 255, 255),
        mass=1e24,
        semi_major_axis=1.0,
        orbital_period=100.0
    )
    
    # Initial position should be at angle 0 (right side of the Sun)
    distance = 1.0 * DISTANCE_SCALE  # semi_major_axis * DISTANCE_SCALE
    expected_x = 960 + distance  # CENTER_X (960) + distance
    expected_y = 500  # CENTER_Y (1000/2)
    
    assert abs(test_planet.x - expected_x) < 1e-6
    assert abs(test_planet.y - expected_y) < 1e-6
    
    # Update position for 1/4 of the orbital period (90 degrees)
    test_planet.update_position(25.0)  # 25 days = 1/4 of 100 days
    
    # After 90 degrees, the planet should be at the top of its orbit
    expected_x_after = 960  # CENTER_X + distance*cos(90°)
    expected_y_after = 500 - distance  # CENTER_Y - distance*sin(90°)
    
    # Allow for some floating point imprecision
    assert abs(test_planet.x - expected_x_after) < 1e-6
    assert abs(test_planet.y - expected_y_after) < 1e-6
