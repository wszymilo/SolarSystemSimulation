"""Tests for the SolarSystem class."""
import pytest
import pygame
from unittest.mock import MagicMock, patch
from src.solar_system import SolarSystem
from src.constants import CELESTIAL_BODIES, SCREEN_WIDTH, SCREEN_HEIGHT


@pytest.fixture
def mock_pygame():
    """Fixture to mock pygame for testing."""
    with patch('pygame.init'), \
         patch('pygame.display.set_mode'), \
         patch('pygame.display.set_caption'), \
         patch('pygame.time.Clock'), \
         patch('pygame.font.init'), \
         patch('pygame.font.SysFont'), \
         patch('pygame.event.get'), \
         patch('pygame.draw.circle'), \
         patch('pygame.display.flip'), \
         patch('pygame.quit'):
        yield


def test_solar_system_initialization(mock_pygame):
    """Test that the SolarSystem initializes correctly."""
    # Create a solar system instance
    solar_system = SolarSystem()
    
    # Verify that pygame was initialized
    pygame.init.assert_called_once()
    pygame.display.set_mode.assert_called_once_with((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption.assert_called_once_with("Solar System Simulation")
    
    # Verify that celestial bodies were created
    assert len(solar_system.bodies) == len(CELESTIAL_BODIES)
    
    # Verify the first body is the Sun
    assert solar_system.bodies[0].name == 'Sun'
    
    # Verify the Sun is at the center
    assert solar_system.bodies[0].x == SCREEN_WIDTH // 2
    assert solar_system.bodies[0].y == SCREEN_HEIGHT // 2


def test_handle_events_quit(mock_pygame):
    """Test handling the quit event."""
    # Create a solar system instance
    solar_system = SolarSystem()
    
    # Mock the event queue to return a QUIT event
    mock_event = MagicMock()
    mock_event.type = pygame.QUIT
    pygame.event.get.return_value = [mock_event]
    
    # Call handle_events
    solar_system.handle_events()
    
    # Verify running is set to False
    assert not solar_system.running


def test_handle_events_escape_key(mock_pygame):
    """Test handling the ESC key press event."""
    # Create a solar system instance
    solar_system = SolarSystem()
    
    # Mock the event queue to return a KEYDOWN event for ESC
    mock_event = MagicMock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_ESCAPE
    pygame.event.get.return_value = [mock_event]
    
    # Initial state should be running
    assert solar_system.running
    
    # Call handle_events
    solar_system.handle_events()
    
    # Verify running is set to False after ESC key press
    assert not solar_system.running


def test_handle_events_pause(mock_pygame):
    """Test handling the pause toggle event."""
    # Create a solar system instance
    solar_system = SolarSystem()
    
    # Mock the event queue to return a KEYDOWN event for SPACE
    mock_event = MagicMock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_SPACE
    pygame.event.get.return_value = [mock_event]
    
    # Initial state should be not paused
    assert not solar_system.paused
    
    # Call handle_events to toggle pause
    solar_system.handle_events()
    
    # Should now be paused
    assert solar_system.paused
    
    # Call handle_events again to toggle back
    solar_system.handle_events()
    
    # Should no longer be paused
    assert not solar_system.paused


def test_update(mock_pygame):
    """Test the update method."""
    # Create a solar system instance
    solar_system = SolarSystem()
    
    # Get a planet (not the Sun)
    planet = next(body for body in solar_system.bodies if body.name != 'Sun')
    
    # Store initial position
    initial_x = planet.x
    initial_y = planet.y
    
    # Call update
    solar_system.update()
    
    # Position should have changed
    assert planet.x != initial_x or planet.y != initial_y
    
    # Test update when paused
    solar_system.paused = True
    initial_x = planet.x
    initial_y = planet.y
    
    solar_system.update()
    
    # Position should not have changed when paused
    assert planet.x == initial_x
    assert planet.y == initial_y


def test_speed_adjustment(mock_pygame):
    """Test speed adjustment with up/down arrows."""
    # Create a solar system instance
    solar_system = SolarSystem()
    
    # Initial speed factor should be 1.0
    assert solar_system.speed_factor == 1.0
    
    # Test speed up
    mock_event = MagicMock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_UP
    pygame.event.get.return_value = [mock_event]
    
    solar_system.handle_events()
    assert solar_system.speed_factor == 2.0  # Should double
    
    # Test speed down
    mock_event.key = pygame.K_DOWN
    solar_system.handle_events()
    assert solar_system.speed_factor == 1.0  # Should halve
    
    # Test minimum speed
    solar_system.speed_factor = 0.2
    solar_system.handle_events()  # Try to go below 0.1
    assert solar_system.speed_factor == 0.1  # Should not go below 0.1


def test_orbit_drawing(mock_pygame):
    """Test that orbits are drawn with the correct scale."""
    # Create a solar system instance
    solar_system = SolarSystem()
    
    # Call the draw method
    solar_system.draw()
    
    # Get all calls to pygame.draw.circle
    draw_calls = pygame.draw.circle.call_args_list
    
    # Find the orbit draw calls (dark gray circles)
    from src.constants import ORBIT_COLOR
    orbit_calls = [
        call for call in draw_calls 
        if call[0][1] == ORBIT_COLOR  # Dark gray color for orbits
    ]
    
    # Verify we have one orbit per non-Sun body
    non_sun_bodies = [b for b in solar_system.bodies if b.name != 'Sun']
    assert len(orbit_calls) == len(non_sun_bodies)
    
    # Check each orbit circle
    for i, body in enumerate(non_sun_bodies):
        call = orbit_calls[i]
        
        # Verify the circle is centered on the screen
        assert call[0][2] == (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Center
        
        # Verify the radius is correct (semi_major_axis * DISTANCE_SCALE)
        expected_radius = int(body.semi_major_axis * 30)  # 30 is DISTANCE_SCALE
        assert call[0][3] == expected_radius, f"Incorrect radius for {body.name}'s orbit"
        
        # Verify line width is 1
        assert call[0][4] == 1, f"Incorrect line width for {body.name}'s orbit"
