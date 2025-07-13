"""Base class for all celestial bodies in the solar system."""
import math
from dataclasses import dataclass, field
from typing import Tuple

import pygame

from src.constants import DISTANCE_SCALE, CENTER_X, CENTER_Y


@dataclass
class CelestialBody:
    """Base class representing a celestial body in the solar system.
    
    Attributes:
        name (str): Name of the celestial body
        radius (float): Radius of the body in km
        color (Tuple[int, int, int]): RGB color tuple for rendering
        mass (float): Mass of the body in kg
        semi_major_axis (float): Semi-major axis of the orbit in AU
        orbital_period (float): Orbital period in Earth days
        eccentricity (float): Eccentricity of the orbit (0 for circular)
    """
    name: str
    radius: float
    color: Tuple[int, int, int]
    mass: float
    semi_major_axis: float = 0.0
    orbital_period: float = 0.0
    eccentricity: float = 0.0
    
    # Position, velocity, and angle will be calculated
    x: float = field(init=False)
    y: float = field(init=False)
    vx: float = field(init=False)
    vy: float = field(init=False)
    angle: float = field(init=False)  # Current angle in radians
    angular_velocity: float = field(init=False)  # Radians per day
    
    def __post_init__(self):
        """Initialize position and velocity based on orbital parameters."""
        if self.orbital_period > 0:  # For planets
            # Initialize angle and angular velocity
            self.angle = 0  # Start at angle 0 (right side of the Sun)
            self.angular_velocity = (2 * math.pi) / self.orbital_period  # Radians per day
            
            # Calculate initial position
            self._update_position()
            
            # Initial velocity (not used in current implementation but kept for future use)
            self.vx = 0
            self.vy = 0
        else:  # For the Sun
            self.x = CENTER_X
            self.y = CENTER_Y
            self.vx = 0
            self.vy = 0
            self.angle = 0
            self.angular_velocity = 0
    
    def _update_position(self):
        """Update the position based on the current angle.
        
        Note: In Pygame, the Y-axis is inverted (increases downward), so we subtract
        the Y-offset from CENTER_Y instead of adding it.
        """
        if self.orbital_period > 0:  # Skip for the Sun
            distance = self.semi_major_axis * DISTANCE_SCALE
            self.x = distance * math.cos(self.angle) + CENTER_X
            self.y = CENTER_Y - distance * math.sin(self.angle)  # Subtract for inverted Y-axis
    
    def update_position(self, dt: float):
        """Update the position of the celestial body.
        
        Args:
            dt: Time step in days
        """
        if self.orbital_period > 0:  # Skip for the Sun
            # Update the angle based on time step
            self.angle += self.angular_velocity * dt
            # Keep the angle between 0 and 2*pi for numerical stability
            self.angle %= 2 * math.pi
            # Update the position based on the new angle
            self._update_position()
    
    def draw(self, screen: pygame.Surface):
        """Draw the celestial body on the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Scale the radius for visualization
        if self.name == 'Sun':
            # Make the Sun more visible but not too large
            scaled_radius = 5
        else:
            # Scale planet sizes relative to Earth's size (Earth = 8 pixels)
            earth_radius = 6371  # km
            base_size = 3  # Increased base size for better visibility
            scaled_radius = max(2, int((self.radius / earth_radius) * base_size))
            
            # Ensure planets are visible but not too large
            scaled_radius = min(scaled_radius, DISTANCE_SCALE)  # Slightly larger cap for better visibility
        
        # Draw the celestial body
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            scaled_radius
        )
        
        # Draw the name
        font = pygame.font.SysFont('Arial', 12)
        text = font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(int(self.x), int(self.y) + scaled_radius + 10))
        screen.blit(text, text_rect)
